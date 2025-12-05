"""
MotiBeam Spatial OS - Ambient Homescreen
Cinematic realm selector with living wall background
"""

import pygame
import sys
import math
from typing import Optional
from core.ui.framework import (
    Theme, Fonts, draw_text_shadowed, draw_glow_circle,
    BreathingAnimation, ParticleSystem, ScrollingTicker,
    format_time, format_date
)
from core.weather import get_current_weather


# Realm definitions
REALMS = [
    {"id": 1, "name": "Daily Flow", "icon": "1", "implemented": False},
    {"id": 2, "name": "Clinical & Health", "icon": "2", "implemented": True},
    {"id": 3, "name": "Learning", "icon": "3", "implemented": False},
    {"id": 4, "name": "Transport", "icon": "4", "implemented": False},
    {"id": 5, "name": "Wellness", "icon": "5", "implemented": False},
    {"id": 6, "name": "Entertainment", "icon": "6", "implemented": False},
    {"id": 7, "name": "Home Control", "icon": "7", "implemented": False},
    {"id": 8, "name": "Security", "icon": "8", "implemented": False},
    {"id": 9, "name": "TeleBeam", "icon": "9", "implemented": True},
]


class MotiBeamOS:
    """Main homescreen - ambient realm selector"""

    def __init__(self):
        pygame.init()

        # Display setup - fullscreen for projection
        self.width = 1920
        self.height = 1080
        self.display = pygame.display.set_mode(
            (self.width, self.height),
            pygame.FULLSCREEN | pygame.NOFRAME
        )
        pygame.display.set_caption("MotiBeam Spatial OS")

        # State
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.selected_realm = 0  # Index into REALMS
        self.privacy_mode = False
        self.show_caregiver_message = False
        self.caregiver_timer = 0

        # Animations
        self.breathing = BreathingAnimation(0.7, 1.0, 0.02)
        self.particles = ParticleSystem(self.width, self.height, max_particles=150)

        # Orb layout (3x3 grid)
        self.orb_positions = self._calculate_orb_positions()

        # Ticker messages
        ticker_messages = [
            "Welcome to MotiBeam Spatial OS",
            "Your ambient computing environment",
            "Use arrow keys to navigate realms",
            "Press Enter to launch a realm",
            "Press P for privacy mode",
            "Press C for caregiver assistance",
            "Built for projection-based ambient computing"
        ]
        self.ticker = ScrollingTicker(self.width, ticker_messages, font_size=Fonts.NORMAL)

        # Weather integration
        # To use real weather API, set environment variable: OPENWEATHER_API_KEY
        # For demo, it will use simulated data
        import os
        api_key = os.environ.get('OPENWEATHER_API_KEY')
        weather_data = get_current_weather(api_key=api_key, location="Home")
        self.weather_temp = weather_data["temp"]
        self.weather_condition = weather_data["condition"]
        self.weather_location = weather_data["location"]
        self.weather_update_timer = 0
        self.weather_update_interval = 3600  # Update every 60 seconds (3600 frames at 60fps)

        # TeleBeam notifications
        self.telebeam_missed_calls = 0
        self.telebeam_new_message = False

    def _calculate_orb_positions(self):
        """Calculate positions for 9 realm orbs in 3x3 grid"""
        positions = []

        # Grid layout
        grid_margin_x = 300
        grid_margin_y = 250
        grid_width = self.width - (grid_margin_x * 2)
        grid_height = self.height - (grid_margin_y * 2) - 150  # Space for ticker

        cell_width = grid_width // 3
        cell_height = grid_height // 3

        for i in range(9):
            row = i // 3
            col = i % 3

            x = grid_margin_x + (col * cell_width) + (cell_width // 2)
            y = grid_margin_y + (row * cell_height) + (cell_height // 2)

            positions.append((x, y))

        return positions

    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                # ESC or Q to quit
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False

                # Arrow navigation
                elif event.key == pygame.K_LEFT:
                    self.selected_realm = (self.selected_realm - 1) % 9
                elif event.key == pygame.K_RIGHT:
                    self.selected_realm = (self.selected_realm + 1) % 9
                elif event.key == pygame.K_UP:
                    self.selected_realm = (self.selected_realm - 3) % 9
                elif event.key == pygame.K_DOWN:
                    self.selected_realm = (self.selected_realm + 3) % 9

                # Number keys (1-9) for direct selection
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    self.selected_realm = event.key - pygame.K_1

                # Enter to launch realm
                elif event.key == pygame.K_RETURN:
                    self.launch_realm(REALMS[self.selected_realm])

                # Privacy mode toggle
                elif event.key == pygame.K_p:
                    self.privacy_mode = not self.privacy_mode

                # Caregiver notification
                elif event.key == pygame.K_c:
                    self.show_caregiver_message = True
                    self.caregiver_timer = 180  # 3 seconds at 60fps

                # TeleBeam demo keys
                elif event.key == pygame.K_i:
                    # Simulate incoming call
                    self.launch_telebeam_incoming()
                elif event.key == pygame.K_m:
                    # Simulate missed call
                    self.telebeam_missed_calls += 1

    def launch_realm(self, realm_data: dict):
        """Launch selected realm"""
        if not realm_data["implemented"]:
            # Show "coming soon" message
            print(f"Realm '{realm_data['name']}' coming soon...")
            return

        realm_id = realm_data["id"]

        if realm_id == 2:
            # Launch Clinical & Health realm
            from realms.clinical_health import ClinicalHealthRealm
            realm = ClinicalHealthRealm(self.display)
            continue_running = realm.run()
            if not continue_running:
                self.running = False

        elif realm_id == 9:
            # Launch TeleBeam
            from realms.telebeam import TeleBeamRealm
            realm = TeleBeamRealm(self.display)
            continue_running = realm.run()
            if not continue_running:
                self.running = False

    def launch_telebeam_incoming(self):
        """Launch TeleBeam with incoming call simulation"""
        from realms.telebeam import TeleBeamRealm
        realm = TeleBeamRealm(self.display, incoming_call=True)
        continue_running = realm.run()
        if not continue_running:
            self.running = False

    def update(self):
        """Update animations and state"""
        self.breathing.update()
        self.particles.update()
        self.ticker.update()

        # Weather update timer
        self.weather_update_timer += 1
        if self.weather_update_timer >= self.weather_update_interval:
            self.weather_update_timer = 0
            # Update weather data
            import os
            api_key = os.environ.get('OPENWEATHER_API_KEY')
            weather_data = get_current_weather(api_key=api_key, location=self.weather_location)
            self.weather_temp = weather_data["temp"]
            self.weather_condition = weather_data["condition"]

        # Caregiver message timer
        if self.show_caregiver_message:
            self.caregiver_timer -= 1
            if self.caregiver_timer <= 0:
                self.show_caregiver_message = False

    def draw(self):
        """Draw homescreen"""
        # Clear with deep background
        self.display.fill(Theme.BG_DEEP)

        # Draw particle system (living wall background)
        self.particles.draw(self.display)

        # Draw realm orbs
        self.draw_realm_orbs()

        # Draw header info
        self.draw_header()

        # Draw ticker
        ticker_y = self.height - 80
        self.ticker.draw(self.display, ticker_y)

        # Draw privacy mode indicator
        if self.privacy_mode:
            self.draw_privacy_indicator()

        # Draw caregiver message
        if self.show_caregiver_message:
            self.draw_caregiver_message()

        # Draw TeleBeam notifications
        if self.telebeam_missed_calls > 0 or self.telebeam_new_message:
            self.draw_telebeam_notification()

    def draw_realm_orbs(self):
        """Draw the 9 realm orbs"""
        breath_val = self.breathing.get_value()

        for i, realm in enumerate(REALMS):
            pos = self.orb_positions[i]
            is_selected = (i == self.selected_realm)

            # Orb appearance
            if is_selected:
                orb_radius = 70
                orb_color = Theme.BLUE_GLOW
                glow_intensity = breath_val
            else:
                orb_radius = 60
                orb_color = Theme.GRAY_MID
                glow_intensity = 0.3

            # Special coloring for TeleBeam with notifications
            if realm["id"] == 9 and (self.telebeam_missed_calls > 0 or self.telebeam_new_message):
                orb_color = Theme.TELEBEAM_UNKNOWN
                glow_intensity = breath_val * 0.8

            # Draw orb with glow
            draw_glow_circle(self.display, pos, orb_radius, orb_color, glow_intensity)

            # Draw realm number
            font = Fonts.get(Fonts.LARGE, bold=True)
            draw_text_shadowed(self.display, realm["icon"], pos, font,
                             Theme.WHITE, shadow_offset=4, center=True)

            # Draw realm name below orb
            name_y = pos[1] + orb_radius + 30
            name_font = Fonts.get(Fonts.SMALL if not is_selected else Fonts.MEDIUM)
            name_color = Theme.WHITE if is_selected else Theme.GRAY_LIGHT

            # Show "COMING SOON" for unimplemented realms
            if not realm["implemented"]:
                display_name = f"{realm['name']}"
                coming_soon_font = Fonts.get(Fonts.SMALL - 8)
                coming_surf = coming_soon_font.render("(Coming Soon)", True, Theme.GRAY_DARK)
                coming_rect = coming_surf.get_rect(center=(pos[0], name_y + 40))
                self.display.blit(coming_surf, coming_rect)
            else:
                display_name = realm['name']

            draw_text_shadowed(self.display, display_name, (pos[0], name_y),
                             name_font, name_color, shadow_offset=2, center=True)

    def draw_header(self):
        """Draw header with time, date, weather"""
        # Time (top left)
        time_str = format_time()
        time_font = Fonts.get(Fonts.LARGE, bold=True)
        draw_text_shadowed(self.display, time_str, (50, 40),
                         time_font, Theme.WHITE, shadow_offset=4)

        # Date (below time)
        date_str = format_date()
        date_font = Fonts.get(Fonts.SMALL)
        draw_text_shadowed(self.display, date_str, (50, 130),
                         date_font, Theme.GRAY_LIGHT, shadow_offset=2)

        # Weather (top right)
        if not self.privacy_mode:
            weather_font = Fonts.get(Fonts.MEDIUM, bold=True)
            weather_str = f"{self.weather_temp} {self.weather_condition}"
            weather_surf = weather_font.render(weather_str, True, Theme.WHITE)
            weather_rect = weather_surf.get_rect(topright=(self.width - 50, 40))

            # Shadow
            shadow_surf = weather_font.render(weather_str, True, (0, 0, 0))
            shadow_rect = shadow_surf.get_rect(topright=(self.width - 47, 43))
            self.display.blit(shadow_surf, shadow_rect)
            self.display.blit(weather_surf, weather_rect)

            # Location
            location_font = Fonts.get(Fonts.SMALL)
            location_surf = location_font.render(self.weather_location, True, Theme.GRAY_LIGHT)
            location_rect = location_surf.get_rect(topright=(self.width - 50, 110))
            self.display.blit(location_surf, location_rect)

        # Title (top center)
        title_font = Fonts.get(Fonts.HUGE, bold=True)
        title_color = Theme.BLUE_SOFT
        draw_text_shadowed(self.display, "MOTIBEAM", (self.width // 2, 50),
                         title_font, title_color, shadow_offset=5, center=True)

    def draw_privacy_indicator(self):
        """Draw privacy mode overlay"""
        font = Fonts.get(Fonts.MEDIUM, bold=True)
        text = "PRIVACY MODE ACTIVE"
        text_surf = font.render(text, True, Theme.AMBER_SOFT)
        text_rect = text_surf.get_rect(center=(self.width // 2, self.height - 150))

        # Subtle background
        bg_rect = text_rect.inflate(40, 20)
        bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (*Theme.AMBER_SOFT, Theme.ALPHA_MEDIUM),
                        (0, 0, bg_rect.width, bg_rect.height), border_radius=10)
        self.display.blit(bg_surf, bg_rect)

        self.display.blit(text_surf, text_rect)

    def draw_caregiver_message(self):
        """Draw caregiver notification"""
        font = Fonts.get(Fonts.LARGE, bold=True)
        text = "CAREGIVER NOTIFIED"
        text_surf = font.render(text, True, Theme.GREEN_SOFT)
        text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2 + 250))

        # Pulsing background
        alpha = int((math.sin(self.caregiver_timer * 0.1) + 1) / 2 * Theme.ALPHA_VISIBLE)
        bg_rect = text_rect.inflate(60, 30)
        bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (*Theme.GREEN_SOFT, alpha),
                        (0, 0, bg_rect.width, bg_rect.height), border_radius=15)
        self.display.blit(bg_surf, bg_rect)

        self.display.blit(text_surf, text_rect)

    def draw_telebeam_notification(self):
        """Draw TeleBeam notification badge on realm #9"""
        # Find TeleBeam orb position
        telebeam_index = 8  # Realm #9 is index 8
        pos = self.orb_positions[telebeam_index]

        # Badge position (top-right of orb)
        badge_x = pos[0] + 50
        badge_y = pos[1] - 50
        badge_radius = 20

        # Draw badge
        breath_val = self.breathing.get_value()
        draw_glow_circle(self.display, (badge_x, badge_y), badge_radius,
                        Theme.TELEBEAM_UNKNOWN, breath_val)

        # Badge number
        if self.telebeam_missed_calls > 0:
            badge_font = Fonts.get(Fonts.SMALL - 8, bold=True)
            badge_text = str(min(self.telebeam_missed_calls, 9))
            if self.telebeam_missed_calls > 9:
                badge_text = "9+"

            badge_surf = badge_font.render(badge_text, True, Theme.WHITE)
            badge_rect = badge_surf.get_rect(center=(badge_x, badge_y))
            self.display.blit(badge_surf, badge_rect)

    def run(self):
        """Main application loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    os = MotiBeamOS()
    os.run()


if __name__ == "__main__":
    main()
