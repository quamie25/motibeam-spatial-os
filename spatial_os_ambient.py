#!/usr/bin/env python3
"""
MotiBeam Spatial OS - Ambient Homescreen
Revolutionary ambient computing platform for OEM licensing

The wall should feel ALIVE - not a computer interface.
Giant visuals readable from 10-15ft, breathing animations, cinema-quality experience.

9 Realms:
1. 🏡 Home & Smart Living
2. ⚕️ Clinical & Health
3. 📚 Education & Learning
4. 🚗 Transport & Automotive
5. 🚨 Emergency Response
6. 🛡️ Security & Surveillance
7. 🏢 Enterprise & Workspace
8. ✈️ Aviation & ATC
9. ⚓ Maritime & Naval

Controls:
- 1-9: Launch realm
- P: Privacy mode
- S: Sleep mode (generative art)
- Q/ESC: Exit
"""

import pygame
import sys
import random
import math
import time as time_module
from datetime import datetime
from typing import List, Tuple

sys.path.insert(0, '/home/user/motibeam-spatial-os')

from core.ui.framework import Theme, UIComponents, Animations, Particle


class RealmOrb:
    """A breathing realm orb with emoji and label"""

    def __init__(self, realm_id: int, emoji: str, name: str, color: Tuple[int, int, int],
                 position: Tuple[int, int], phase_offset: float):
        self.realm_id = realm_id
        self.emoji = emoji
        self.name = name
        self.color = color
        self.position = position
        self.phase_offset = phase_offset
        self.base_radius = 80
        self.selected = False
        self.hover_scale = 1.0

    def update(self, dt: float, mouse_pos: Tuple[int, int]):
        """Update orb state"""
        # Check hover
        dx = mouse_pos[0] - self.position[0]
        dy = mouse_pos[1] - self.position[1]
        distance = math.sqrt(dx * dx + dy * dy)

        target_scale = 1.2 if distance < 100 else 1.0
        self.hover_scale += (target_scale - self.hover_scale) * dt * 5

    def draw(self, surface: pygame.Surface, time: float, ui: UIComponents, font_emoji, font_label):
        """Draw breathing orb with emoji"""
        # Breathing pulse
        pulse = math.sin(time * 2 + self.phase_offset) * 0.15 + 1.0
        radius = int(self.base_radius * pulse * self.hover_scale)

        # Glow layers
        for i in range(6):
            glow_radius = radius + (i * 15)
            glow_alpha = max(0, 80 - i * 13)
            glow_color = (*self.color, glow_alpha)
            s = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, glow_color, (glow_radius, glow_radius), glow_radius)
            surface.blit(s, (self.position[0] - glow_radius, self.position[1] - glow_radius))

        # Main orb
        pygame.draw.circle(surface, self.color, self.position, radius)

        # Inner glow
        inner_radius = int(radius * 0.7)
        inner_glow = (*self.color, 100)
        s = pygame.Surface((inner_radius * 2, inner_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, inner_glow, (inner_radius, inner_radius), inner_radius)
        surface.blit(s, (self.position[0] - inner_radius, self.position[1] - inner_radius))

        # Draw realm ID as large text instead of emoji (emojis show as ?)
        # Use realm number prominently
        id_text = font_emoji.render(str(self.realm_id), True, (255, 255, 255))
        id_rect = id_text.get_rect(center=self.position)
        surface.blit(id_text, id_rect)

        # Realm number INSIDE orb (top) - PROMINENT
        num_y_inside = self.position[1] - int(radius * 0.4)
        ui.draw_text_with_shadow(
            surface, str(self.realm_id), font_label,
            (self.position[0], num_y_inside),
            (255, 255, 255), 3, True
        )

        # Realm name below orb
        label_y = self.position[1] + int(radius) + 40
        ui.draw_text_with_shadow(
            surface, self.name, font_label,
            (self.position[0], label_y),
            (255, 255, 255), 2, True
        )


class TickerMessage:
    """Scrolling information ticker message"""

    def __init__(self, text: str, x: float):
        self.text = text
        self.x = x


class SpatialOSAmbient:
    """MotiBeam Spatial OS - Ambient Homescreen"""

    def __init__(self):
        pygame.init()

        # Fullscreen display
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption("MotiBeam Spatial OS")

        print(f"🌌 MotiBeam Spatial OS initializing at {self.width}x{self.height}")

        # Clock for 60 FPS
        self.clock = pygame.time.Clock()
        self.running = False
        self.time = 0.0

        # Theme and UI
        self.theme = Theme()
        self.ui = UIComponents()
        self.anim = Animations()

        # Load fonts (3x larger for projector)
        try:
            self.font_time = pygame.font.Font(None, 280)      # Giant clock
            self.font_date = pygame.font.Font(None, 100)      # Date
            self.font_title = pygame.font.Font(None, 140)     # Title
            self.font_subtitle = pygame.font.Font(None, 70)   # Subtitle
            self.font_label = pygame.font.Font(None, 50)      # Labels
            self.font_ticker = pygame.font.Font(None, 55)     # Ticker

            # Try emoji font
            try:
                self.font_emoji = pygame.font.Font('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 100)
            except:
                self.font_emoji = self.font_title
        except Exception as e:
            print(f"Font loading error: {e}")
            self.font_time = pygame.font.Font(None, 280)
            self.font_date = pygame.font.Font(None, 100)
            self.font_title = pygame.font.Font(None, 140)
            self.font_subtitle = pygame.font.Font(None, 70)
            self.font_label = pygame.font.Font(None, 50)
            self.font_ticker = pygame.font.Font(None, 55)
            self.font_emoji = self.font_title

        # Modes
        self.privacy_mode = False
        self.sleep_mode = False

        # Realm selector (optional keyboard navigation)
        self.selected_realm = 2  # Default to Clinical realm (implemented)
        self.selector_visible = True

        # Initialize 9 realm orbs
        self.init_realm_orbs()

        # Ambient particles (living wall effect)
        self.particles: List[Particle] = []
        self.particle_spawn_timer = 0.0

        # Information ticker
        self.ticker_messages = [
            "MotiBeam Spatial OS - Revolutionary Ambient Computing Platform",
            "9 Specialized Realms for Smart Living, Healthcare, Education & More",
            "Cinema-Quality Visuals - Designed for 10-15ft Viewing Distance",
            "Breathing Animations - The Wall Feels ALIVE",
            "Press 1-9 to Enter Realms - P for Privacy - S for Sleep Mode",
        ]
        self.ticker_x = self.width
        self.current_ticker_index = 0
        self.ticker_speed = 120  # pixels per second

        print("✨ MotiBeam Spatial OS ready!")

    def init_realm_orbs(self):
        """Initialize 9 realm orbs in a 3x3 grid with proper spacing"""
        realm_data = [
            (1, "HOME", "HOME", self.theme.REALM_COLORS[1]),           # 🏡
            (2, "CLINICAL", "CLINICAL", self.theme.REALM_COLORS[2]),   # ⚕️
            (3, "EDUCATION", "EDUCATION", self.theme.REALM_COLORS[3]), # 📚
            (4, "TRANSPORT", "TRANSPORT", self.theme.REALM_COLORS[4]), # 🚗
            (5, "EMERGENCY", "EMERGENCY", self.theme.REALM_COLORS[5]), # 🚨
            (6, "SECURITY", "SECURITY", self.theme.REALM_COLORS[6]),   # 🛡️
            (7, "ENTERPRISE", "ENTERPRISE", self.theme.REALM_COLORS[7]), # 🏢
            (8, "AVIATION", "AVIATION", self.theme.REALM_COLORS[8]),   # ✈️
            (9, "MARITIME", "MARITIME", self.theme.REALM_COLORS[9]),   # ⚓
        ]

        # Calculate grid layout (3x3) with more spacing to prevent overlap
        orb_area_top = 420
        orb_area_height = self.height - orb_area_top - 180

        grid_cols = 3
        grid_rows = 3

        # Increase spacing - divide available space more generously
        spacing_x = self.width // 4  # More horizontal space
        spacing_y = orb_area_height // 4  # More vertical space

        # Center the grid
        start_x = (self.width - (spacing_x * 2)) // 2
        start_y = orb_area_top + 40

        self.orbs = []
        for i, (realm_id, emoji, name, color) in enumerate(realm_data):
            row = i // grid_cols
            col = i % grid_cols

            x = start_x + (spacing_x * col)
            y = start_y + (spacing_y * row)

            phase_offset = i * 0.7
            orb = RealmOrb(realm_id, emoji, name, color, (x, y), phase_offset)
            self.orbs.append(orb)

    def run(self):
        """Main ambient homescreen loop"""
        self.running = True

        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.time += dt

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keypress(event.key)

            # Update
            self.update(dt)

            # Render
            self.render()

            pygame.display.flip()

        pygame.quit()
        sys.exit(0)

    def update(self, dt: float):
        """Update ambient homescreen"""
        # Update realm orbs
        mouse_pos = pygame.mouse.get_pos()
        for orb in self.orbs:
            orb.update(dt, mouse_pos)

        # Update particles
        self.update_particles(dt)

        # Update ticker
        self.update_ticker(dt)

    def update_particles(self, dt: float):
        """Update ambient particles"""
        # Spawn new particles
        self.particle_spawn_timer += dt
        if self.particle_spawn_timer > 0.15:
            self.particle_spawn_timer = 0.0
            self.spawn_particle()

        # Update existing particles
        for particle in self.particles[:]:
            particle.update(dt, self.width, self.height)
            if particle.is_dead():
                self.particles.remove(particle)

    def spawn_particle(self):
        """Spawn a new ambient particle"""
        x = random.randint(0, self.width)
        y = random.randint(400, self.height - 150)
        vx = random.uniform(-30, 30)
        vy = random.uniform(-30, 30)
        color = random.choice(self.theme.PARTICLE_COLORS)
        size = random.randint(2, 5)

        particle = Particle(x, y, vx, vy, color, size)
        self.particles.append(particle)

    def update_ticker(self, dt: float):
        """Update information ticker"""
        self.ticker_x -= self.ticker_speed * dt

        # Get current message
        current_message = self.ticker_messages[self.current_ticker_index]
        message_width = self.font_ticker.size(current_message)[0]

        # Reset when message scrolls off screen
        if self.ticker_x < -message_width:
            self.ticker_x = self.width
            self.current_ticker_index = (self.current_ticker_index + 1) % len(self.ticker_messages)

    def render(self):
        """Render ambient homescreen"""
        # Background
        self.screen.fill(self.theme.BG_DEEP)

        if self.privacy_mode:
            self.render_privacy_mode()
        elif self.sleep_mode:
            self.render_sleep_mode()
        else:
            self.render_normal_mode()

    def render_normal_mode(self):
        """Render normal ambient mode"""
        # Ambient particles (living wall)
        for particle in self.particles:
            particle.draw(self.screen)

        # Giant clock at top
        self.render_clock()

        # 9 Realm orbs
        for orb in self.orbs:
            orb.draw(self.screen, self.time, self.ui, self.font_emoji, self.font_label)

            # Draw selector highlight on selected realm
            if self.selector_visible and orb.realm_id == self.selected_realm:
                self.draw_realm_selector(orb)

        # Information ticker at bottom
        self.render_ticker()

        # Instructions (subtle)
        self.render_instructions()

    def render_clock(self):
        """Render giant clock readable from 10-15ft"""
        now = datetime.now()

        # Time (massive)
        time_str = now.strftime("%H:%M")
        seconds_str = now.strftime(":%S")

        # Draw time with breathing glow
        pulse = self.anim.breathe(self.time, 1.5)

        # Glow effect
        for i in range(5):
            glow_offset = i * 3
            glow_alpha = max(0, 100 - i * 20)
            glow_surf = self.font_time.render(time_str, True, (*self.theme.ACCENT_GLOW, glow_alpha))
            glow_rect = glow_surf.get_rect(center=(self.width // 2 + glow_offset, 140 + glow_offset))
            self.screen.blit(glow_surf, glow_rect)

        # Main time
        time_surf = self.font_time.render(time_str, True, self.theme.TEXT_BRIGHT)
        time_rect = time_surf.get_rect(center=(self.width // 2, 140))
        self.screen.blit(time_surf, time_rect)

        # Seconds (smaller, dimmer)
        seconds_surf = self.font_date.render(seconds_str, True, self.theme.TEXT_DIM)
        seconds_rect = seconds_surf.get_rect(midleft=(time_rect.right + 20, 140))
        self.screen.blit(seconds_surf, seconds_rect)

        # Date
        date_str = now.strftime("%A, %B %d, %Y")
        self.ui.draw_text_with_shadow(
            self.screen, date_str, self.font_date,
            (self.width // 2, 260), self.theme.TEXT_NORMAL, 3, True
        )

    def render_ticker(self):
        """Render information ticker"""
        ticker_y = self.height - 100

        # Ticker background bar
        bar_height = 80
        pygame.draw.rect(self.screen, self.theme.BG_MID,
                        (0, ticker_y - 20, self.width, bar_height))

        # Ticker message (text only - emojis cause rendering issues)
        current_message = self.ticker_messages[self.current_ticker_index]
        ticker_surf = self.font_ticker.render(current_message, True, self.theme.ACCENT_PRIMARY)
        self.screen.blit(ticker_surf, (int(self.ticker_x), ticker_y))

    def render_instructions(self):
        """Render subtle instructions"""
        instructions = "1-9 or ARROWS: SELECT  │  ENTER: LAUNCH  │  P: PRIVACY  │  S: SLEEP  │  Q: EXIT"

        self.ui.draw_text_with_shadow(
            self.screen, instructions, self.font_label,
            (self.width // 2, self.height - 40),
            self.theme.TEXT_DARK, 2, True
        )

    def render_privacy_mode(self):
        """Render privacy mode (blank screen with minimal info)"""
        self.screen.fill((0, 0, 0))

        # Subtle "Privacy Mode" text
        privacy_text = "PRIVACY MODE"
        self.ui.draw_text_with_shadow(
            self.screen, privacy_text, self.font_subtitle,
            (self.width // 2, self.height // 2),
            (60, 60, 60), 2, True
        )

        # Minimal clock
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        self.ui.draw_text_with_shadow(
            self.screen, time_str, self.font_date,
            (self.width // 2, self.height // 2 + 80),
            (80, 80, 80), 2, True
        )

    def draw_realm_selector(self, orb: RealmOrb):
        """Draw pulsing selector highlight around selected realm orb"""
        pulse = self.anim.breathe(self.time * 2, 3.0)  # Faster pulse for selector
        base_radius = orb.base_radius * orb.hover_scale

        # Multiple pulsing rings
        for i in range(3):
            ring_radius = int(base_radius * pulse * (1.0 + i * 0.1)) + 20 + (i * 10)
            ring_width = max(2, int(5 - i))
            ring_alpha = max(0, int((180 - i * 40) * pulse))
            ring_color = (*orb.color, ring_alpha)

            # Draw ring
            s = pygame.Surface((ring_radius * 2 + 20, ring_radius * 2 + 20), pygame.SRCALPHA)
            pygame.draw.circle(s, ring_color, (ring_radius + 10, ring_radius + 10), ring_radius, ring_width)
            self.screen.blit(s, (orb.position[0] - ring_radius - 10, orb.position[1] - ring_radius - 10))

        # Selection indicator text below orb
        indicator_y = orb.position[1] + int(base_radius) + 100
        self.ui.draw_text_with_shadow(
            self.screen, "◄ SELECTED ►", self.font_label,
            orb.position, orb.color, 3, True
        )

    def render_sleep_mode(self):
        """Render sleep mode with generative art"""
        self.screen.fill(self.theme.BG_DEEP)

        # Generative art: flowing waves
        wave_count = 8
        for i in range(wave_count):
            y_base = (self.height // wave_count) * i + (self.height // (wave_count * 2))

            points = []
            for x in range(0, self.width + 20, 20):
                wave1 = math.sin(x * 0.01 + self.time * 0.5 + i * 0.5) * 60
                wave2 = math.sin(x * 0.005 + self.time * 0.3 + i * 0.3) * 40
                y = y_base + wave1 + wave2
                points.append((x, int(y)))

            if len(points) > 1:
                color_index = i % len(self.theme.PARTICLE_COLORS)
                color = self.theme.PARTICLE_COLORS[color_index][:3]
                alpha = 40 + int(math.sin(self.time + i) * 20)

                for j in range(1, len(points)):
                    s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                    pygame.draw.line(s, (*color, alpha), points[j - 1], points[j], 3)
                    self.screen.blit(s, (0, 0))

    def handle_keypress(self, key: int):
        """Handle keyboard input"""
        # Toggle modes
        if key == pygame.K_p:
            self.privacy_mode = not self.privacy_mode
            print(f"🔒 Privacy mode: {self.privacy_mode}")

        elif key == pygame.K_s:
            self.sleep_mode = not self.sleep_mode
            print(f"😴 Sleep mode: {self.sleep_mode}")

        # Exit
        elif key == pygame.K_q or key == pygame.K_ESCAPE:
            print("👋 Exiting MotiBeam Spatial OS")
            self.running = False

        # Arrow key navigation
        elif key == pygame.K_LEFT:
            self.selected_realm = max(1, self.selected_realm - 1)
            self.selector_visible = True
        elif key == pygame.K_RIGHT:
            self.selected_realm = min(9, self.selected_realm + 1)
            self.selector_visible = True
        elif key == pygame.K_UP:
            self.selected_realm = max(1, self.selected_realm - 3)  # Move up a row
            self.selector_visible = True
        elif key == pygame.K_DOWN:
            self.selected_realm = min(9, self.selected_realm + 3)  # Move down a row
            self.selector_visible = True

        # Launch selected realm with ENTER
        elif key == pygame.K_RETURN or key == pygame.K_SPACE:
            self.launch_realm(self.selected_realm)

        # Launch realms directly with number keys
        elif pygame.K_1 <= key <= pygame.K_9:
            realm_num = key - pygame.K_0
            self.selected_realm = realm_num  # Update selector
            self.launch_realm(realm_num)

    def launch_realm(self, realm_num: int):
        """Launch a specific realm"""
        realm_names = {
            1: "Home", 2: "Clinical", 3: "Education", 4: "Transport",
            5: "Emergency", 6: "Security", 7: "Enterprise", 8: "Aviation", 9: "Maritime"
        }
        realm_name = realm_names.get(realm_num, f"Realm {realm_num}")
        print(f"🚀 Launching {realm_name}...")

        # Special handling for Clinical realm (only one implemented)
        if realm_num == 2:
            try:
                # Test import BEFORE quitting pygame
                print(f"   Checking Clinical realm availability...")
                try:
                    from realms.clinical_health import ClinicalHealthPro
                    print(f"   ✓ Clinical realm loaded")
                except ImportError as ie:
                    print(f"   ❌ Import error: {ie}")
                    print(f"   Make sure pygame is installed: pip3 install pygame")
                    self.show_temp_message(f"ERROR: Cannot load Clinical realm\n{str(ie)}\n\nInstall: pip3 install pygame", 4.0)
                    return

                # Save current state
                saved_time = self.time

                # Launch Clinical realm (NO pygame.quit() - realm manages its own display)
                print(f"   Entering {realm_name} realm...")
                clinical = ClinicalHealthPro()
                result = clinical.run()

                # Restore homescreen display when returning
                print(f"↩️  Returned from realm {result}, restoring homescreen...")

                # Reinitialize homescreen (this recreates the display)
                self.__init__()
                self.time = saved_time  # Restore time to avoid jarring animation jumps

                print("✅ Homescreen restored")

            except KeyboardInterrupt:
                print("\n⚠️  Realm interrupted by user")
                # Reinitialize homescreen
                pygame.init()
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.__init__()

            except Exception as e:
                print(f"❌ Error launching Clinical realm: {e}")
                import traceback
                traceback.print_exc()

                # Try to recover by reinitializing homescreen
                try:
                    pygame.init()
                    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    self.__init__()
                    print("✅ Homescreen recovered after error")
                except:
                    print("❌ Fatal error - cannot recover homescreen")
                    self.running = False

        else:
            # Placeholder for other realms
            print(f"⚠️  {realm_name} realm not yet implemented")
            print(f"   Building all 9 realms coming soon!")

            # Show a message on screen
            self.show_temp_message(f"{realm_name.upper()}\nCOMING SOON", 2.0)

    def show_temp_message(self, message: str, duration: float = 2.0):
        """Show a temporary message overlay"""
        start_time = time_module.time()

        while time_module.time() - start_time < duration:
            dt = self.clock.tick(60) / 1000.0
            self.time += dt

            # Handle events to avoid freezing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    return  # Exit message early on any key

            # Continue normal render
            self.render_normal_mode()

            # Overlay message
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            self.ui.draw_text_with_shadow(
                self.screen, message, self.font_title,
                (self.width // 2, self.height // 2),
                self.theme.ACCENT_PRIMARY, 4, True
            )

            pygame.display.flip()


def main():
    """Run MotiBeam Spatial OS Ambient Homescreen"""
    print("=" * 60)
    print("MOTIBEAM SPATIAL OS - AMBIENT HOMESCREEN")
    print("Revolutionary Ambient Computing Platform")
    print("=" * 60)

    ambient = SpatialOSAmbient()
    ambient.run()


if __name__ == "__main__":
    main()
