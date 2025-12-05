#!/usr/bin/env python3
"""
MotiBeam Spatial OS - Main Launcher
Dark ambient "living wall" 3×3 realm selector
"""

import pygame
import sys
import math
from datetime import datetime
import random

# Initialize Pygame
pygame.init()

# Display setup
DISPLAY_INFO = pygame.display.Info()
SCREEN_WIDTH = DISPLAY_INFO.current_w
SCREEN_HEIGHT = DISPLAY_INFO.current_h

# DARK ambient color palette (living wall, not bright screen)
COLORS = {
    'bg_deep': (5, 8, 12),                # Deep space black
    'bg_ambient': (12, 18, 25),           # Subtle ambient glow
    'card_bg': (25, 35, 50, 220),         # Strong opaque card
    'card_border': (60, 80, 110),         # Visible border
    'card_selected': (100, 140, 180),     # Clear highlight
    'text_primary': (220, 230, 245),      # Bright readable white
    'text_secondary': (160, 180, 200),    # Visible gray-blue
    'ticker_color': (180, 200, 220),      # Bright ticker
    'accent_home': (80, 160, 200),        # Brighter cyan
    'accent_health': (80, 180, 140),      # Brighter green
    'accent_education': (140, 100, 200),  # Brighter purple
    'accent_transport': (200, 150, 80),   # Brighter orange
    'accent_emergency': (220, 90, 90),    # Brighter red
    'accent_security': (80, 130, 200),    # Brighter blue
    'accent_enterprise': (140, 150, 160), # Brighter gray
    'accent_aviation': (100, 160, 220),   # Brighter sky blue
    'accent_maritime': (80, 170, 180),    # Brighter teal
    'particle_glow': (80, 120, 160, 100), # Visible particle
}

# Realm definitions with LETTER PAIRS (no emoji issues)
REALMS = [
    {
        'id': 1,
        'name': 'Home',
        'subtitle': 'Smart Home',
        'icon': 'HO',
        'color': COLORS['accent_home'],
        'scene_file': 'scenes.home_realm'
    },
    {
        'id': 2,
        'name': 'Clinical',
        'subtitle': 'Health & Wellness',
        'icon': 'CL',
        'color': COLORS['accent_health'],
        'scene_file': 'scenes.clinical_realm'
    },
    {
        'id': 3,
        'name': 'Education',
        'subtitle': 'Learning Hub',
        'icon': 'ED',
        'color': COLORS['accent_education'],
        'scene_file': 'scenes.education_realm'
    },
    {
        'id': 4,
        'name': 'Transport',
        'subtitle': 'Automotive HUD',
        'icon': 'TR',
        'color': COLORS['accent_transport'],
        'scene_file': 'scenes.transport_realm'
    },
    {
        'id': 5,
        'name': 'Emergency',
        'subtitle': 'Crisis Response',
        'icon': 'EM',
        'color': COLORS['accent_emergency'],
        'scene_file': 'scenes.emergency_realm'
    },
    {
        'id': 6,
        'name': 'Security',
        'subtitle': 'Surveillance',
        'icon': 'SE',
        'color': COLORS['accent_security'],
        'scene_file': 'scenes.security_realm'
    },
    {
        'id': 7,
        'name': 'Enterprise',
        'subtitle': 'Workspace',
        'icon': 'EN',
        'color': COLORS['accent_enterprise'],
        'scene_file': 'scenes.enterprise_realm'
    },
    {
        'id': 8,
        'name': 'Aviation',
        'subtitle': 'Flight Systems',
        'icon': 'AV',
        'color': COLORS['accent_aviation'],
        'scene_file': 'scenes.aviation_realm'
    },
    {
        'id': 9,
        'name': 'Maritime',
        'subtitle': 'Navigation',
        'icon': 'MA',
        'color': COLORS['accent_maritime'],
        'scene_file': 'scenes.maritime_realm'
    }
]


class AmbientParticle:
    """Glowing particle for living wall background"""
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.speed = random.uniform(0.2, 0.5)
        self.size = random.randint(2, 5)
        self.opacity = random.randint(60, 120)
        self.direction = random.uniform(0, 2 * math.pi)
        self.pulse_offset = random.uniform(0, math.pi * 2)

    def update(self, width, height, time_pulse):
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed

        # Wrap around screen
        if self.x < 0:
            self.x = width
        elif self.x > width:
            self.x = 0
        if self.y < 0:
            self.y = height
        elif self.y > height:
            self.y = 0

    def draw(self, surface, time_pulse):
        # Pulsing glow effect
        pulse = math.sin(time_pulse * 0.02 + self.pulse_offset)
        current_opacity = int(self.opacity + 30 * pulse)
        current_opacity = max(40, min(150, current_opacity))

        color = (
            COLORS['particle_glow'][0],
            COLORS['particle_glow'][1],
            COLORS['particle_glow'][2],
            current_opacity
        )

        s = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
        # Outer glow
        pygame.draw.circle(s, color, (self.size * 2, self.size * 2), self.size * 2)
        # Inner bright core
        core_color = (
            min(255, COLORS['particle_glow'][0] + 40),
            min(255, COLORS['particle_glow'][1] + 40),
            min(255, COLORS['particle_glow'][2] + 40),
            current_opacity
        )
        pygame.draw.circle(s, core_color, (self.size * 2, self.size * 2), self.size)
        surface.blit(s, (int(self.x) - self.size * 2, int(self.y) - self.size * 2))


class ScrollingTicker:
    """Large, bright scrolling ticker"""
    def __init__(self, width, height, font):
        self.width = width
        self.height = height
        self.font = font
        self.messages = [
            "Welcome to MotiBeam Spatial OS  •  ",
            "Navigate: Arrow Keys or Numbers 1-9  •  ",
            "Privacy Mode: Press P  •  ",
            "Exit: Press ESC  •  "
        ]
        self.full_message = "".join(self.messages)
        self.x_offset = width
        self.speed = 2
        self.text_surface = self.font.render(
            self.full_message,
            True,
            COLORS['ticker_color']
        )

    def update(self):
        self.x_offset -= self.speed
        if self.x_offset < -self.text_surface.get_width():
            self.x_offset = self.width

    def draw(self, surface):
        if self.text_surface:
            y_pos = self.height - 50
            surface.blit(self.text_surface, (self.x_offset, y_pos))
            # Draw second copy for seamless loop
            if self.x_offset < 0:
                surface.blit(
                    self.text_surface,
                    (self.x_offset + self.text_surface.get_width() + 100, y_pos)
                )


class WeatherDisplay:
    """Simulated weather display"""
    def __init__(self):
        self.location = "Cypress, TX"
        self.temp = 72
        self.condition = "Clear"
        self.last_update = datetime.now()

    def update(self):
        now = datetime.now()
        if (now - self.last_update).seconds > 300:
            self.temp += random.choice([-1, 0, 0, 1])
            self.last_update = now

    def get_display_text(self):
        return f"{self.location}  •  {self.temp}°F  •  {self.condition}"


class SpatialOS:
    """Main launcher application"""
    def __init__(self):
        # Screen setup
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
        )
        pygame.display.set_caption("MotiBeam Spatial OS")

        # Fonts (elder-friendly, large sizes)
        self.font_title = pygame.font.SysFont('Arial', 64, bold=True)
        self.font_subtitle = pygame.font.SysFont('Arial', 28)
        self.font_card_icon = pygame.font.SysFont('Arial', 80, bold=True)
        self.font_card_title = pygame.font.SysFont('Arial', 44, bold=True)
        self.font_card_subtitle = pygame.font.SysFont('Arial', 26)
        self.font_time = pygame.font.SysFont('Arial', 52, bold=True)
        self.font_date = pygame.font.SysFont('Arial', 26)
        self.font_ticker = pygame.font.SysFont('Arial', 32, bold=True)

        # State
        self.selected_realm = 0
        self.privacy_mode = False
        self.running = True
        self.clock = pygame.time.Clock()
        self.time_pulse = 0

        # Ambient particles (more for living wall effect)
        self.particles = [AmbientParticle(SCREEN_WIDTH, SCREEN_HEIGHT)
                         for _ in range(80)]

        # Ticker
        self.ticker = ScrollingTicker(SCREEN_WIDTH, SCREEN_HEIGHT, self.font_ticker)

        # Weather
        self.weather = WeatherDisplay()

        # Card layout (better centered)
        self.card_width = 360
        self.card_height = 190
        self.card_margin = 50
        self.grid_start_x = (SCREEN_WIDTH - (self.card_width * 3 + self.card_margin * 2)) // 2
        self.grid_start_y = 240  # Start lower for better centering

    def get_card_position(self, index):
        """Get (x, y) position for card at index (0-8)"""
        row = index // 3
        col = index % 3
        x = self.grid_start_x + col * (self.card_width + self.card_margin)
        y = self.grid_start_y + row * (self.card_height + self.card_margin)
        return (x, y)

    def draw_card(self, realm, index, selected=False):
        """Draw a realm card"""
        x, y = self.get_card_position(index)

        # Card background with strong opacity
        card_surf = pygame.Surface((self.card_width, self.card_height), pygame.SRCALPHA)

        if selected:
            # Breathing glow for selected card
            glow_intensity = int(30 + 20 * math.sin(self.time_pulse * 0.05))
            border_color = tuple(min(255, c + glow_intensity) for c in COLORS['card_selected'])

            # Add glow around selected card
            glow_surf = pygame.Surface(
                (self.card_width + 20, self.card_height + 20),
                pygame.SRCALPHA
            )
            glow_color = (*COLORS['card_selected'], 80)
            pygame.draw.rect(
                glow_surf, glow_color,
                (0, 0, self.card_width + 20, self.card_height + 20),
                border_radius=20
            )
            self.screen.blit(glow_surf, (x - 10, y - 10))

            pygame.draw.rect(card_surf, COLORS['card_bg'],
                           (0, 0, self.card_width, self.card_height), border_radius=12)
            pygame.draw.rect(card_surf, border_color,
                           (0, 0, self.card_width, self.card_height), 4, border_radius=12)
        else:
            pygame.draw.rect(card_surf, COLORS['card_bg'],
                           (0, 0, self.card_width, self.card_height), border_radius=12)
            pygame.draw.rect(card_surf, COLORS['card_border'],
                           (0, 0, self.card_width, self.card_height), 2, border_radius=12)

        self.screen.blit(card_surf, (x, y))

        # Letter pair icon (large, always visible)
        icon_surf = self.font_card_icon.render(realm['icon'], True, realm['color'])
        icon_x = x + (self.card_width - icon_surf.get_width()) // 2
        icon_y = y + 20
        self.screen.blit(icon_surf, (icon_x, icon_y))

        # Card title
        title_surf = self.font_card_title.render(realm['name'], True, COLORS['text_primary'])
        title_x = x + (self.card_width - title_surf.get_width()) // 2
        title_y = y + 110
        self.screen.blit(title_surf, (title_x, title_y))

        # Card subtitle
        subtitle_surf = self.font_card_subtitle.render(realm['subtitle'], True, COLORS['text_secondary'])
        subtitle_x = x + (self.card_width - subtitle_surf.get_width()) // 2
        subtitle_y = y + 155
        self.screen.blit(subtitle_surf, (subtitle_x, subtitle_y))

    def draw_header(self):
        """Draw compact header"""
        # Title (moved up, more compact)
        title_surf = self.font_title.render("MOTIBEAM SPATIAL OS", True, COLORS['text_primary'])
        title_x = (SCREEN_WIDTH - title_surf.get_width()) // 2
        self.screen.blit(title_surf, (title_x, 25))

        # Subtitle
        subtitle_surf = self.font_subtitle.render(
            "Select Realm  •  Navigate with Arrows",
            True,
            COLORS['text_secondary']
        )
        subtitle_x = (SCREEN_WIDTH - subtitle_surf.get_width()) // 2
        self.screen.blit(subtitle_surf, (subtitle_x, 95))

        # Time (top right)
        now = datetime.now()
        time_str = now.strftime("%I:%M %p").lstrip('0')
        time_surf = self.font_time.render(time_str, True, COLORS['text_primary'])
        time_x = SCREEN_WIDTH - time_surf.get_width() - 40
        self.screen.blit(time_surf, (time_x, 25))

        # Date
        date_str = now.strftime("%a, %b %d")
        date_surf = self.font_date.render(date_str, True, COLORS['text_secondary'])
        date_x = SCREEN_WIDTH - date_surf.get_width() - 40
        self.screen.blit(date_surf, (date_x, 82))

        # Weather
        weather_str = self.weather.get_display_text()
        weather_surf = self.font_date.render(weather_str, True, COLORS['text_secondary'])
        weather_x = SCREEN_WIDTH - weather_surf.get_width() - 40
        self.screen.blit(weather_surf, (weather_x, 110))

    def draw_footer(self):
        """Draw bottom status bar"""
        # Privacy mode indicator
        privacy_text = "Privacy: ON" if self.privacy_mode else "Privacy: OFF"
        privacy_surf = self.font_date.render(privacy_text, True, COLORS['text_secondary'])
        self.screen.blit(privacy_surf, (40, SCREEN_HEIGHT - 90))

        # Mode indicator
        mode_text = "Mode: NORMAL"
        mode_surf = self.font_date.render(mode_text, True, COLORS['text_secondary'])
        self.screen.blit(mode_surf, (40, SCREEN_HEIGHT - 60))

    def draw_background(self):
        """Draw dark living wall background"""
        # Solid deep black base
        self.screen.fill(COLORS['bg_deep'])

        # Subtle radial ambient glow from center
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        max_radius = max(SCREEN_WIDTH, SCREEN_HEIGHT)

        for i in range(5):
            radius = max_radius * (i + 1) / 5
            alpha = int(15 * (5 - i) / 5)
            glow_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            color = (*COLORS['bg_ambient'], alpha)
            pygame.draw.circle(glow_surf, color, (center_x, center_y), int(radius))
            self.screen.blit(glow_surf, (0, 0))

        # Draw glowing particles
        for particle in self.particles:
            particle.update(SCREEN_WIDTH, SCREEN_HEIGHT, self.time_pulse)
            particle.draw(self.screen, self.time_pulse)

    def handle_input(self):
        """Handle keyboard input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_LEFT:
                    if self.selected_realm % 3 > 0:
                        self.selected_realm -= 1
                elif event.key == pygame.K_RIGHT:
                    if self.selected_realm % 3 < 2:
                        self.selected_realm += 1
                elif event.key == pygame.K_UP:
                    if self.selected_realm >= 3:
                        self.selected_realm -= 3
                elif event.key == pygame.K_DOWN:
                    if self.selected_realm < 6:
                        self.selected_realm += 3

                elif event.key in range(pygame.K_1, pygame.K_9 + 1):
                    realm_num = event.key - pygame.K_1
                    if realm_num < len(REALMS):
                        self.selected_realm = realm_num

                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.launch_realm(self.selected_realm)

                elif event.key == pygame.K_p:
                    self.privacy_mode = not self.privacy_mode

    def launch_realm(self, index):
        """Launch the selected realm"""
        realm = REALMS[index]
        print(f"\n🚀 Launching realm: {realm['name']}")
        print(f"   Scene file: {realm['scene_file']}")

        try:
            module_name = realm['scene_file']
            module = __import__(module_name, fromlist=[''])

            if hasattr(module, 'run'):
                module.run(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
            elif hasattr(module, 'Realm'):
                realm_instance = module.Realm(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                realm_instance.run()
            else:
                print(f"⚠️  Realm module found but no run() function or Realm class")

        except ModuleNotFoundError:
            print(f"⚠️  Realm not implemented yet: {realm['scene_file']}")
        except Exception as e:
            print(f"❌ Error launching realm: {e}")

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_input()

            # Update
            self.time_pulse += 1
            self.ticker.update()
            self.weather.update()

            # Draw
            self.draw_background()
            self.draw_header()

            # Draw all cards
            for i, realm in enumerate(REALMS):
                selected = (i == self.selected_realm)
                self.draw_card(realm, i, selected)

            self.draw_footer()
            self.ticker.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = SpatialOS()
    app.run()
