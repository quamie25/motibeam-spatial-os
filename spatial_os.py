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
    'card_bg': (30, 42, 60, 115),         # Brighter, 45% opacity for projection
    'card_border': (80, 100, 130),        # More visible border
    'card_selected': (120, 160, 200),     # Brighter highlight
    'text_primary': (255, 255, 255),      # Full white text
    'text_secondary': (200, 215, 235),    # Brighter secondary text
    'ticker_color': (220, 235, 250),      # High contrast ticker
    'accent_home': (80, 160, 200),        # Brighter cyan
    'accent_health': (80, 180, 140),      # Brighter green
    'accent_education': (140, 100, 200),  # Brighter purple
    'accent_transport': (200, 150, 80),   # Brighter orange
    'accent_emergency': (220, 90, 90),    # Brighter red
    'accent_security': (80, 130, 200),    # Brighter blue
    'accent_enterprise': (140, 150, 160), # Brighter gray
    'accent_aviation': (100, 160, 220),   # Brighter sky blue
    'accent_maritime': (80, 170, 180),    # Brighter teal
    'particle_glow': (120, 160, 200, 150), # BRIGHTER particles (Option C)
    'badge_bg': (220, 90, 90, 200),       # Notification badge background
    'badge_text': (255, 255, 255),        # Badge text
    'number_badge': (140, 160, 180, 200), # Brighter number badge
    'emoji_glow': (200, 220, 255, 100),   # Glow behind emojis
}

# Realm definitions with EMOJIS
REALMS = [
    {
        'id': 1,
        'name': 'Home',
        'subtitle': 'Smart Home',
        'emoji': '🏠',
        'fallback': 'HO',
        'color': COLORS['accent_home'],
        'scene_file': 'scenes.home_realm'
    },
    {
        'id': 2,
        'name': 'Clinical',
        'subtitle': 'Health & Wellness',
        'emoji': '🏥',
        'fallback': 'CL',
        'color': COLORS['accent_health'],
        'scene_file': 'scenes.clinical_realm'
    },
    {
        'id': 3,
        'name': 'Education',
        'subtitle': 'Learning Hub',
        'emoji': '📚',
        'fallback': 'ED',
        'color': COLORS['accent_education'],
        'scene_file': 'scenes.education_realm'
    },
    {
        'id': 4,
        'name': 'Transport',
        'subtitle': 'Automotive HUD',
        'emoji': '🚗',
        'fallback': 'TR',
        'color': COLORS['accent_transport'],
        'scene_file': 'scenes.transport_realm'
    },
    {
        'id': 5,
        'name': 'Emergency',
        'subtitle': 'Crisis Response',
        'emoji': '🚨',
        'fallback': 'EM',
        'color': COLORS['accent_emergency'],
        'scene_file': 'scenes.emergency_realm'
    },
    {
        'id': 6,
        'name': 'Security',
        'subtitle': 'Surveillance',
        'emoji': '🛡️',
        'fallback': 'SE',
        'color': COLORS['accent_security'],
        'scene_file': 'scenes.security_realm'
    },
    {
        'id': 7,
        'name': 'Enterprise',
        'subtitle': 'Workspace',
        'emoji': '🏢',
        'fallback': 'EN',
        'color': COLORS['accent_enterprise'],
        'scene_file': 'scenes.enterprise_realm'
    },
    {
        'id': 8,
        'name': 'Aviation',
        'subtitle': 'Flight Systems',
        'emoji': '✈️',
        'fallback': 'AV',
        'color': COLORS['accent_aviation'],
        'scene_file': 'scenes.aviation_realm'
    },
    {
        'id': 9,
        'name': 'Maritime',
        'subtitle': 'Navigation',
        'emoji': '⚓',
        'fallback': 'MA',
        'color': COLORS['accent_maritime'],
        'scene_file': 'scenes.maritime_realm'
    }
]


class AmbientParticle:
    """Glowing particle for living wall background - BRIGHTER for Option C"""
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.speed = random.uniform(0.3, 0.7)
        self.size = random.randint(3, 7)      # Larger particles
        self.opacity = random.randint(100, 180) # Much brighter
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
        # Pulsing glow effect - BRIGHTER
        pulse = math.sin(time_pulse * 0.02 + self.pulse_offset)
        current_opacity = int(self.opacity + 40 * pulse)
        current_opacity = max(80, min(220, current_opacity))  # Much brighter range

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
    """Dynamic, intelligent scrolling ticker"""
    def __init__(self, width, height, font):
        self.width = width
        self.height = height
        self.font = font
        # Dynamic contextual alerts
        self.messages = [
            "Clinical: BP check at 3:00 PM",
            "TeleBeam: 2 missed calls",
            "Home: Package delivered",
            "Focus: Review medications",
            "Security: All systems normal",
            "Press 1-9 to select realm"
        ]
        self.full_message = "  •  ".join(self.messages) + "  •  "
        self.x_offset = width
        self.speed = 1.8  # Slower scroll for readability
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
    """Simulated weather display with icon"""
    def __init__(self):
        self.location = "Cypress, TX"
        self.temp = 72
        self.condition = "Clear"
        self.last_update = datetime.now()
        self.weather_icons = {
            'Clear': '☀️',
            'Sunny': '☀️',
            'Cloudy': '☁️',
            'Partly Cloudy': '⛅',
            'Rain': '🌧️',
            'Snow': '❄️',
            'Storm': '⛈️'
        }

    def update(self):
        now = datetime.now()
        if (now - self.last_update).seconds > 300:
            self.temp += random.choice([-1, 0, 0, 1])
            self.last_update = now

    def get_icon(self):
        return self.weather_icons.get(self.condition, '☀️')

    def get_display_text(self):
        icon = self.get_icon()
        return f"{icon} {self.temp}°F  •  {self.location}"


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
        self.font_card_title = pygame.font.SysFont('Arial', 44, bold=True)
        self.font_card_subtitle = pygame.font.SysFont('Arial', 26)
        self.font_time = pygame.font.SysFont('Arial', 52, bold=True)
        self.font_date = pygame.font.SysFont('Arial', 26)
        self.font_ticker = pygame.font.SysFont('Arial', 36, bold=True)  # Larger ticker
        self.font_badge = pygame.font.SysFont('Arial', 20, bold=True)   # Number badges
        self.font_notification = pygame.font.SysFont('Arial', 18, bold=True)  # Notification count

        # Try multiple emoji fonts for best compatibility - LARGER (20% increase)
        emoji_fonts = ['Noto Color Emoji', 'Apple Color Emoji', 'Segoe UI Emoji', 'Symbola', 'DejaVu Sans']
        self.font_emoji = None
        for font_name in emoji_fonts:
            try:
                self.font_emoji = pygame.font.SysFont(font_name, 86)  # 72 * 1.2 = ~86
                break
            except:
                continue

        # Fallback to regular font if no emoji font found
        if self.font_emoji is None:
            self.font_emoji = pygame.font.SysFont('Arial', 86)

        # Fallback font for letter pairs (also larger)
        self.font_card_icon = pygame.font.SysFont('Arial', 96, bold=True)

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

        # Notifications (simulated for now)
        self.notifications = {
            'home': 2,  # 2 missed calls/messages
            'clinical': 1,  # 1 upcoming appointment
        }

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

        # Try emoji first with GLOW, fall back to letter pair if it fails
        try:
            emoji_surf = self.font_emoji.render(realm['emoji'], True, realm['color'])
            # Check if emoji actually rendered (not just "?")
            test_surf = self.font_emoji.render('?', True, realm['color'])
            if emoji_surf.get_size() != test_surf.get_size():
                # Emoji rendered successfully! Add glow behind it
                icon_x = x + (self.card_width - emoji_surf.get_width()) // 2
                icon_y = y + 10

                # Draw glow effect behind emoji
                glow_size = 100
                glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, COLORS['emoji_glow'],
                                 (glow_size//2, glow_size//2), glow_size//2)
                glow_x = x + (self.card_width - glow_size) // 2
                glow_y = y + 15
                self.screen.blit(glow_surf, (glow_x, glow_y))

                # Draw emoji on top of glow
                self.screen.blit(emoji_surf, (icon_x, icon_y))
            else:
                # Emoji rendered as "?", use fallback
                raise Exception("Emoji not supported")
        except:
            # Use letter pair fallback with glow
            icon_surf = self.font_card_icon.render(realm['fallback'], True, realm['color'])
            icon_x = x + (self.card_width - icon_surf.get_width()) // 2
            icon_y = y + 15

            # Add glow for letter pairs too
            glow_size = 100
            glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, COLORS['emoji_glow'],
                             (glow_size//2, glow_size//2), glow_size//2)
            glow_x = x + (self.card_width - glow_size) // 2
            glow_y = y + 20
            self.screen.blit(glow_surf, (glow_x, glow_y))

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

        # Number badge (bottom-right corner)
        badge_number = str(index + 1)
        badge_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(badge_surf, COLORS['number_badge'], (16, 16), 16)
        badge_text = self.font_badge.render(badge_number, True, COLORS['text_primary'])
        badge_text_x = (32 - badge_text.get_width()) // 2
        badge_text_y = (32 - badge_text.get_height()) // 2
        badge_surf.blit(badge_text, (badge_text_x, badge_text_y))
        self.screen.blit(badge_surf, (x + self.card_width - 40, y + self.card_height - 40))

        # Notification badge (top-right corner) - only for specific realms
        realm_key = realm['name'].lower()
        if realm_key in self.notifications and self.notifications[realm_key] > 0:
            notif_count = self.notifications[realm_key]
            notif_surf = pygame.Surface((28, 28), pygame.SRCALPHA)

            # Pulsing effect for notifications
            pulse = math.sin(self.time_pulse * 0.08)
            pulse_size = int(28 + 4 * pulse)
            pulse_alpha = int(200 + 55 * pulse)

            notif_color = (*COLORS['badge_bg'][:3], pulse_alpha)
            pygame.draw.circle(notif_surf, notif_color, (14, 14), 14)

            notif_text = self.font_notification.render(str(notif_count), True, COLORS['badge_text'])
            notif_text_x = (28 - notif_text.get_width()) // 2
            notif_text_y = (28 - notif_text.get_height()) // 2
            notif_surf.blit(notif_text, (notif_text_x, notif_text_y))
            self.screen.blit(notif_surf, (x + self.card_width - 35, y + 8))

    def draw_header(self):
        """Draw compact header"""
        # Title (moved up, more compact)
        title_surf = self.font_title.render("MOTIBEAM SPATIAL OS", True, COLORS['text_primary'])
        title_x = (SCREEN_WIDTH - title_surf.get_width()) // 2
        self.screen.blit(title_surf, (title_x, 25))

        # Simple subtitle (minimal reading)
        subtitle_surf = self.font_subtitle.render(
            "Select Realm",
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
        """Draw bottom status with icon-only privacy indicator"""
        # Privacy indicator - ICON ONLY (no text)
        if self.privacy_mode:
            privacy_icon = "🔒"
            privacy_color = (150, 255, 150)  # Bright green when ON
        else:
            privacy_icon = "🔓"
            privacy_color = COLORS['text_secondary']

        privacy_surf = self.font_time.render(privacy_icon, True, privacy_color)
        self.screen.blit(privacy_surf, (40, SCREEN_HEIGHT - 100))

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
