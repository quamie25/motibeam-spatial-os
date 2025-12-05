#!/usr/bin/env python3
"""
MotiBeam Spatial OS - Main Launcher
Soft, projection-friendly 3×3 realm selector
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

# Soft color palette (projection-friendly)
COLORS = {
    'bg_dark': (15, 20, 30),           # Deep blue-black
    'bg_ambient': (25, 35, 50),        # Subtle lighter blue
    'card_bg': (35, 45, 65, 180),      # Soft translucent card
    'card_border': (80, 100, 130),     # Muted border
    'card_selected': (120, 140, 170),  # Soft highlight
    'text_primary': (200, 210, 230),   # Soft white
    'text_secondary': (140, 155, 180), # Muted gray-blue
    'accent_home': (100, 160, 180),    # Soft cyan
    'accent_health': (100, 160, 130),  # Soft green
    'accent_education': (130, 100, 170), # Soft purple
    'accent_transport': (160, 130, 100), # Soft orange
    'accent_emergency': (180, 100, 100), # Soft red
    'accent_security': (100, 130, 160), # Soft blue
    'accent_enterprise': (130, 130, 140), # Soft gray
    'accent_aviation': (100, 140, 170), # Soft sky blue
    'accent_maritime': (90, 140, 150),  # Soft teal
}

# Realm definitions (9 cards)
REALMS = [
    {
        'id': 1,
        'name': 'Home',
        'subtitle': 'Smart Home',
        'emoji': '🏠',
        'color': COLORS['accent_home'],
        'scene_file': 'scenes.home_realm'
    },
    {
        'id': 2,
        'name': 'Clinical',
        'subtitle': 'Health & Wellness',
        'emoji': '🏥',
        'color': COLORS['accent_health'],
        'scene_file': 'scenes.clinical_realm'
    },
    {
        'id': 3,
        'name': 'Education',
        'subtitle': 'Learning Hub',
        'emoji': '📚',
        'color': COLORS['accent_education'],
        'scene_file': 'scenes.education_realm'
    },
    {
        'id': 4,
        'name': 'Transport',
        'subtitle': 'Automotive HUD',
        'emoji': '🚗',
        'color': COLORS['accent_transport'],
        'scene_file': 'scenes.transport_realm'
    },
    {
        'id': 5,
        'name': 'Emergency',
        'subtitle': 'Crisis Response',
        'emoji': '🚨',
        'color': COLORS['accent_emergency'],
        'scene_file': 'scenes.emergency_realm'
    },
    {
        'id': 6,
        'name': 'Security',
        'subtitle': 'Surveillance',
        'emoji': '🛡️',
        'color': COLORS['accent_security'],
        'scene_file': 'scenes.security_realm'
    },
    {
        'id': 7,
        'name': 'Enterprise',
        'subtitle': 'Workspace',
        'emoji': '🏢',
        'color': COLORS['accent_enterprise'],
        'scene_file': 'scenes.enterprise_realm'
    },
    {
        'id': 8,
        'name': 'Aviation',
        'subtitle': 'Flight Systems',
        'emoji': '✈️',
        'color': COLORS['accent_aviation'],
        'scene_file': 'scenes.aviation_realm'
    },
    {
        'id': 9,
        'name': 'Maritime',
        'subtitle': 'Navigation',
        'emoji': '⚓',
        'color': COLORS['accent_maritime'],
        'scene_file': 'scenes.maritime_realm'
    }
]


class AmbientParticle:
    """Subtle floating particle for background ambience"""
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.speed = random.uniform(0.1, 0.3)
        self.size = random.randint(1, 3)
        self.opacity = random.randint(20, 60)
        self.direction = random.uniform(0, 2 * math.pi)

    def update(self, width, height):
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

    def draw(self, surface):
        color = (COLORS['text_secondary'][0], COLORS['text_secondary'][1],
                COLORS['text_secondary'][2], self.opacity)
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (self.size, self.size), self.size)
        surface.blit(s, (int(self.x) - self.size, int(self.y) - self.size))


class ScrollingTicker:
    """Large scrolling ticker for bottom of screen"""
    def __init__(self, width, height, font):
        self.width = width
        self.height = height
        self.font = font
        self.messages = [
            "Welcome to MotiBeam Spatial OS",
            "Navigate with Arrow Keys or Number Keys (1-9)",
            "Press P to toggle Privacy Mode",
            "Press F to toggle Fullscreen",
            "Press ESC to exit"
        ]
        self.current_message = 0
        self.x_offset = width
        self.speed = 2
        self.text_surface = None
        self.render_current_message()

    def render_current_message(self):
        self.text_surface = self.font.render(
            self.messages[self.current_message],
            True,
            COLORS['text_secondary']
        )

    def update(self):
        self.x_offset -= self.speed
        if self.x_offset < -self.text_surface.get_width():
            self.current_message = (self.current_message + 1) % len(self.messages)
            self.render_current_message()
            self.x_offset = self.width

    def draw(self, surface):
        if self.text_surface:
            surface.blit(self.text_surface, (self.x_offset, self.height - 60))


class WeatherDisplay:
    """Simulated weather display (can be wired to real API later)"""
    def __init__(self):
        self.location = "Cypress, TX"
        self.temp = 72
        self.condition = "Clear"
        self.last_update = datetime.now()

    def update(self):
        # Simulate slight temperature variation
        now = datetime.now()
        if (now - self.last_update).seconds > 300:  # Update every 5 min
            self.temp += random.choice([-1, 0, 0, 1])
            self.last_update = now

    def get_display_text(self):
        return f"{self.location} • {self.temp}°F • {self.condition}"


class SpatialOS:
    """Main launcher application"""
    def __init__(self):
        # Screen setup
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
        )
        pygame.display.set_caption("MotiBeam Spatial OS")

        # Fonts (elder-friendly sizes)
        self.font_title = pygame.font.SysFont('Arial', 72, bold=True)
        self.font_subtitle = pygame.font.SysFont('Arial', 32)
        self.font_card_title = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_card_subtitle = pygame.font.SysFont('Arial', 28)
        self.font_time = pygame.font.SysFont('Arial', 56, bold=True)
        self.font_date = pygame.font.SysFont('Arial', 28)
        self.font_ticker = pygame.font.SysFont('Arial', 36)
        self.font_emoji = pygame.font.SysFont('Segoe UI Emoji', 64)

        # State
        self.selected_realm = 0  # 0-8 for the 9 realms
        self.privacy_mode = False
        self.running = True
        self.clock = pygame.time.Clock()
        self.time_pulse = 0  # For subtle breathing animation

        # Ambient particles
        self.particles = [AmbientParticle(SCREEN_WIDTH, SCREEN_HEIGHT)
                         for _ in range(50)]

        # Ticker
        self.ticker = ScrollingTicker(SCREEN_WIDTH, SCREEN_HEIGHT, self.font_ticker)

        # Weather
        self.weather = WeatherDisplay()

        # Card layout (3x3 grid)
        self.card_width = 380
        self.card_height = 200
        self.card_margin = 40
        self.grid_start_x = (SCREEN_WIDTH - (self.card_width * 3 + self.card_margin * 2)) // 2
        self.grid_start_y = 200

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

        # Card background (translucent)
        card_surf = pygame.Surface((self.card_width, self.card_height), pygame.SRCALPHA)

        if selected:
            # Soft breathing glow for selected card
            glow_intensity = int(20 + 15 * math.sin(self.time_pulse * 0.05))
            border_color = tuple(min(255, c + glow_intensity) for c in COLORS['card_selected'])
            pygame.draw.rect(card_surf, COLORS['card_bg'],
                           (0, 0, self.card_width, self.card_height), border_radius=15)
            pygame.draw.rect(card_surf, border_color,
                           (0, 0, self.card_width, self.card_height), 3, border_radius=15)
        else:
            pygame.draw.rect(card_surf, COLORS['card_bg'],
                           (0, 0, self.card_width, self.card_height), border_radius=15)
            pygame.draw.rect(card_surf, COLORS['card_border'],
                           (0, 0, self.card_width, self.card_height), 2, border_radius=15)

        self.screen.blit(card_surf, (x, y))

        # Emoji icon (top center)
        try:
            emoji_surf = self.font_emoji.render(realm['emoji'], True, realm['color'])
            emoji_x = x + (self.card_width - emoji_surf.get_width()) // 2
            emoji_y = y + 20
            self.screen.blit(emoji_surf, (emoji_x, emoji_y))
        except:
            # Fallback if emoji doesn't render
            fallback_text = realm['name'][0:2].upper()
            fallback_surf = self.font_card_title.render(fallback_text, True, realm['color'])
            fallback_x = x + (self.card_width - fallback_surf.get_width()) // 2
            fallback_y = y + 30
            self.screen.blit(fallback_surf, (fallback_x, fallback_y))

        # Card title
        title_surf = self.font_card_title.render(realm['name'], True, COLORS['text_primary'])
        title_x = x + (self.card_width - title_surf.get_width()) // 2
        title_y = y + 105
        self.screen.blit(title_surf, (title_x, title_y))

        # Card subtitle
        subtitle_surf = self.font_card_subtitle.render(realm['subtitle'], True, COLORS['text_secondary'])
        subtitle_x = x + (self.card_width - subtitle_surf.get_width()) // 2
        subtitle_y = y + 155
        self.screen.blit(subtitle_surf, (subtitle_x, subtitle_y))

    def draw_header(self):
        """Draw top header with title, time, date"""
        # Title
        title_surf = self.font_title.render("MOTIBEAM SPATIAL OS", True, COLORS['text_primary'])
        title_x = (SCREEN_WIDTH - title_surf.get_width()) // 2
        self.screen.blit(title_surf, (title_x, 30))

        # Subtitle
        subtitle_surf = self.font_subtitle.render("Select Realm • Navigate with Arrows", True, COLORS['text_secondary'])
        subtitle_x = (SCREEN_WIDTH - subtitle_surf.get_width()) // 2
        self.screen.blit(subtitle_surf, (subtitle_x, 115))

        # Time (top right)
        now = datetime.now()
        time_str = now.strftime("%I:%M %p").lstrip('0')
        time_surf = self.font_time.render(time_str, True, COLORS['text_primary'])
        time_x = SCREEN_WIDTH - time_surf.get_width() - 50
        self.screen.blit(time_surf, (time_x, 30))

        # Date (below time)
        date_str = now.strftime("%a, %b %d")
        date_surf = self.font_date.render(date_str, True, COLORS['text_secondary'])
        date_x = SCREEN_WIDTH - date_surf.get_width() - 50
        self.screen.blit(date_surf, (date_x, 95))

        # Weather (below date)
        weather_str = self.weather.get_display_text()
        weather_surf = self.font_date.render(weather_str, True, COLORS['text_secondary'])
        weather_x = SCREEN_WIDTH - weather_surf.get_width() - 50
        self.screen.blit(weather_surf, (weather_x, 130))

    def draw_footer(self):
        """Draw bottom status bar"""
        # Privacy mode indicator (bottom left)
        privacy_text = "🔒 Privacy: ON" if self.privacy_mode else "🔓 Privacy: OFF"
        privacy_surf = self.font_date.render(privacy_text, True, COLORS['text_secondary'])
        self.screen.blit(privacy_surf, (40, SCREEN_HEIGHT - 100))

        # Mode indicator
        mode_text = "Mode: NORMAL"
        mode_surf = self.font_date.render(mode_text, True, COLORS['text_secondary'])
        self.screen.blit(mode_surf, (40, SCREEN_HEIGHT - 60))

    def draw_background(self):
        """Draw ambient background"""
        # Base gradient (dark to slightly lighter)
        for y in range(SCREEN_HEIGHT):
            blend = y / SCREEN_HEIGHT
            color = (
                int(COLORS['bg_dark'][0] + (COLORS['bg_ambient'][0] - COLORS['bg_dark'][0]) * blend),
                int(COLORS['bg_dark'][1] + (COLORS['bg_ambient'][1] - COLORS['bg_dark'][1]) * blend),
                int(COLORS['bg_dark'][2] + (COLORS['bg_ambient'][2] - COLORS['bg_dark'][2]) * blend)
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))

        # Draw particles
        for particle in self.particles:
            particle.update(SCREEN_WIDTH, SCREEN_HEIGHT)
            particle.draw(self.screen)

    def handle_input(self):
        """Handle keyboard input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                # ESC to exit
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                # Arrow keys for navigation
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

                # Number keys (1-9) for direct selection
                elif event.key in range(pygame.K_1, pygame.K_9 + 1):
                    realm_num = event.key - pygame.K_1
                    if realm_num < len(REALMS):
                        self.selected_realm = realm_num

                # ENTER or SPACE to launch selected realm
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.launch_realm(self.selected_realm)

                # P to toggle privacy mode
                elif event.key == pygame.K_p:
                    self.privacy_mode = not self.privacy_mode

                # F to toggle fullscreen (already fullscreen, but for future)
                elif event.key == pygame.K_f:
                    pass  # Already in fullscreen, but could toggle windowed mode

    def launch_realm(self, index):
        """Launch the selected realm"""
        realm = REALMS[index]
        print(f"\n🚀 Launching realm: {realm['name']}")
        print(f"   Scene file: {realm['scene_file']}")

        try:
            # Try to import and run the realm
            module_name = realm['scene_file']
            module = __import__(module_name, fromlist=[''])

            # Look for a run() function or Realm class
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
