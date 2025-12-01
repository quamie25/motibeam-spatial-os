#!/usr/bin/env python3
"""
MotiBeam Spatial OS - Interactive Grid Launcher
3x3 realm grid with global mode and theme controls

Controls:
    Arrows/WASD - Navigate grid
    ENTER/SPACE - Launch realm
    M - Cycle mode (Normal → Study → Sleep)
    T - Cycle theme (Neon → Minimal → Night)
    F - Toggle fullscreen
    ESC/Q - Quit
"""

import sys
import os
import pygame
import importlib
import logging

from core.global_state import global_state
from config.realms_config import REALMS_CONFIG

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class SpatialOSLauncher:
    """Interactive 3x3 grid launcher for MotiBeam Spatial OS"""

    def __init__(self):
        pygame.init()

        # Display setup
        self.display_info = pygame.display.Info()
        self.setup_display()

        pygame.display.set_caption("MotiBeam Spatial OS")
        self.clock = pygame.time.Clock()
        self.running = True

        # Grid configuration (3x3)
        self.grid_layout = [
            ['home', 'clinical', 'education'],
            ['transport', 'emergency', 'security'],
            ['enterprise', 'aviation', 'maritime']
        ]

        # Selection state
        self.selected_row = 0
        self.selected_col = 0

        # Realm cache
        self.realm_instances = {}

        # Animation state
        self.anim_time = 0

    def setup_display(self):
        """Setup display based on global fullscreen state"""
        if global_state.fullscreen:
            flags = pygame.FULLSCREEN | pygame.NOFRAME
            self.screen = pygame.display.set_mode(
                (self.display_info.current_w, self.display_info.current_h),
                flags
            )
        else:
            windowed_w = int(self.display_info.current_w * 0.8)
            windowed_h = int(self.display_info.current_h * 0.8)
            self.screen = pygame.display.set_mode((windowed_w, windowed_h))

        self.width, self.height = self.screen.get_size()

    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        global_state.fullscreen = not global_state.fullscreen
        self.setup_display()
        logger.info(f"Fullscreen: {global_state.fullscreen}")

    def get_realm_info(self, realm_id):
        """Get realm display information"""
        realm_data = {
            'home': {'name': 'Home', 'emoji': '🏡', 'subtitle': 'Smart Living'},
            'clinical': {'name': 'Clinical', 'emoji': '🩺', 'subtitle': 'Health & Wellness'},
            'education': {'name': 'Education', 'emoji': '📚', 'subtitle': 'Learning & Focus'},
            'transport': {'name': 'Transport', 'emoji': '🚗', 'subtitle': 'Automotive HUD'},
            'emergency': {'name': 'Emergency', 'emoji': '🚨', 'subtitle': '911 Dispatch'},
            'security': {'name': 'Security', 'emoji': '🛡️', 'subtitle': 'Surveillance'},
            'enterprise': {'name': 'Enterprise', 'emoji': '🏢', 'subtitle': 'Workspace'},
            'aviation': {'name': 'Aviation', 'emoji': '✈️', 'subtitle': 'Air Traffic'},
            'maritime': {'name': 'Maritime', 'emoji': '⚓', 'subtitle': 'Navigation'}
        }
        return realm_data.get(realm_id, {'name': realm_id, 'emoji': '?', 'subtitle': ''})

    def draw_grid(self):
        """Draw the 3x3 realm grid"""
        theme = global_state.get_theme_colors()
        mode_config = global_state.get_mode_config()

        # Background
        bg_color = tuple(int(c * mode_config['background_alpha']) for c in theme['bg'])
        self.screen.fill(bg_color)

        # Draw animated background circles (subtle)
        self.draw_background_circles(mode_config)

        # Title
        try:
            title_font = pygame.font.Font(None, 96)
            subtitle_font = pygame.font.Font(None, 42)
            status_font = pygame.font.Font(None, 36)
        except:
            title_font = pygame.font.SysFont('arial', 96, bold=True)
            subtitle_font = pygame.font.SysFont('arial', 42)
            status_font = pygame.font.SysFont('arial', 36)

        # Title text
        title_surf = title_font.render("MOTIBEAM SPATIAL OS", True, theme['primary'])
        title_rect = title_surf.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title_surf, title_rect)

        # Subtitle
        subtitle_text = "Select Realm · Navigate with Arrows"
        subtitle_surf = subtitle_font.render(subtitle_text, True, theme['secondary'])
        subtitle_rect = subtitle_surf.get_rect(center=(self.width // 2, 140))
        self.screen.blit(subtitle_surf, subtitle_rect)

        # Grid area
        grid_start_y = 220
        grid_width = self.width - 200
        grid_height = self.height - grid_start_y - 120

        tile_width = grid_width // 3 - 40
        tile_height = grid_height // 3 - 40

        # Draw tiles
        for row in range(3):
            for col in range(3):
                realm_id = self.grid_layout[row][col]
                is_selected = (row == self.selected_row and col == self.selected_col)

                x = 100 + col * (tile_width + 40) + (grid_width - (tile_width * 3 + 80)) // 2
                y = grid_start_y + row * (tile_height + 40)

                self.draw_tile(x, y, tile_width, tile_height, realm_id, is_selected, theme, mode_config)

        # Status bar at bottom
        self.draw_status_bar(theme, status_font)

    def draw_tile(self, x, y, w, h, realm_id, is_selected, theme, mode_config):
        """Draw a single realm tile"""
        info = self.get_realm_info(realm_id)

        # Tile background
        if is_selected:
            # Pulsing selection effect
            pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500
            alpha = int(60 + 40 * pulse * mode_config['animation_intensity'])
            border_width = 4
        else:
            alpha = 30
            border_width = 2

        # Draw tile background with transparency
        tile_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(tile_surf, (*theme['accent_base'], alpha), (0, 0, w, h), border_radius=15)
        pygame.draw.rect(tile_surf, theme['accent_base'], (0, 0, w, h), border_width, border_radius=15)
        self.screen.blit(tile_surf, (x, y))

        # Emoji icon
        try:
            emoji_font = pygame.font.Font(None, 120)
        except:
            emoji_font = pygame.font.SysFont('arial', 120)

        emoji_surf = emoji_font.render(info['emoji'], True, theme['primary'])
        emoji_rect = emoji_surf.get_rect(center=(x + w // 2, y + h // 2 - 30))
        self.screen.blit(emoji_surf, emoji_rect)

        # Realm name
        try:
            name_font = pygame.font.Font(None, 48)
            sub_font = pygame.font.Font(None, 32)
        except:
            name_font = pygame.font.SysFont('arial', 48, bold=True)
            sub_font = pygame.font.SysFont('arial', 32)

        name_surf = name_font.render(info['name'], True, theme['primary'])
        name_rect = name_surf.get_rect(center=(x + w // 2, y + h - 60))
        self.screen.blit(name_surf, name_rect)

        # Subtitle
        sub_surf = sub_font.render(info['subtitle'], True, theme['secondary'])
        sub_rect = sub_surf.get_rect(center=(x + w // 2, y + h - 25))
        self.screen.blit(sub_surf, sub_rect)

    def draw_background_circles(self, mode_config):
        """Draw subtle animated background circles"""
        import math

        circles = [
            (0.15, 0.25, 180),
            (0.85, 0.30, 220),
            (0.50, 0.75, 200),
        ]

        theme = global_state.get_theme_colors()

        for base_x, base_y, base_r in circles:
            # Breathing animation
            phase = self.anim_time * 0.3
            radius = int(base_r + 25 * math.sin(phase) * mode_config['circle_speed_multiplier'])

            x = int(base_x * self.width)
            y = int(base_y * self.height)

            # Very subtle glow
            alpha = int(8 * mode_config['circle_alpha_multiplier'])
            s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*theme['accent_base'], alpha), (radius, radius), radius)
            self.screen.blit(s, (x - radius, y - radius), special_flags=pygame.BLEND_ADD)

    def draw_status_bar(self, theme, font):
        """Draw status bar with mode, theme, and controls"""
        y = self.height - 60

        # Left: Mode
        mode_text = f"Mode: {global_state.mode}"
        mode_surf = font.render(mode_text, True, theme['accent_base'])
        self.screen.blit(mode_surf, (50, y))

        # Center: Theme
        theme_text = f"Theme: {global_state.theme}"
        theme_surf = font.render(theme_text, True, theme['accent_base'])
        theme_rect = theme_surf.get_rect(center=(self.width // 2, y))
        self.screen.blit(theme_surf, theme_rect)

        # Right: Controls hint
        controls_text = "M=Mode · T=Theme · F=Fullscreen · Q=Quit"
        controls_surf = font.render(controls_text, True, theme['secondary'])
        controls_rect = controls_surf.get_rect(right=self.width - 50, centery=y)
        self.screen.blit(controls_surf, controls_rect)

    def handle_navigation(self, key):
        """Handle arrow key / WASD navigation"""
        if key in [pygame.K_UP, pygame.K_w]:
            self.selected_row = (self.selected_row - 1) % 3
        elif key in [pygame.K_DOWN, pygame.K_s]:
            self.selected_row = (self.selected_row + 1) % 3
        elif key in [pygame.K_LEFT, pygame.K_a]:
            self.selected_col = (self.selected_col - 1) % 3
        elif key in [pygame.K_RIGHT, pygame.K_d]:
            self.selected_col = (self.selected_col + 1) % 3

    def launch_realm(self):
        """Launch the currently selected realm"""
        realm_id = self.grid_layout[self.selected_row][self.selected_col]
        logger.info(f"Launching realm: {realm_id}")

        try:
            # Load realm
            realm = self.load_realm(realm_id)
            if realm:
                # Run realm (it should handle its own event loop)
                realm.run(duration=60)  # 60 seconds default

                # Re-setup display after returning (realm might have changed it)
                self.setup_display()

        except Exception as e:
            logger.error(f"Failed to launch realm {realm_id}: {e}")
            import traceback
            traceback.print_exc()

    def load_realm(self, realm_id):
        """Load and cache a realm instance"""
        if realm_id in self.realm_instances:
            realm = self.realm_instances[realm_id]
            realm.screen = self.screen
            return realm

        try:
            config = REALMS_CONFIG[realm_id]
            module_path = config['module_path']
            class_name = config['class_name']

            # Import module
            module = importlib.import_module(module_path)
            realm_class = getattr(module, class_name)

            # Instantiate
            realm = realm_class(standalone=False)
            realm.screen = self.screen
            realm.initialize()

            # Cache
            self.realm_instances[realm_id] = realm
            return realm

        except Exception as e:
            logger.error(f"Failed to load realm {realm_id}: {e}")
            return None

    def run(self):
        """Main launcher loop"""
        logger.info("MotiBeam Spatial OS Launcher starting...")
        logger.info(f"Mode: {global_state.mode}, Theme: {global_state.theme}")

        while self.running:
            dt = self.clock.tick(30) / 1000.0
            self.anim_time += dt

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    # Quit
                    if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                        self.running = False

                    # Navigation
                    elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                                      pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                        self.handle_navigation(event.key)

                    # Launch realm
                    elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        self.launch_realm()

                    # Mode toggle
                    elif event.key == pygame.K_m:
                        new_mode = global_state.cycle_mode()
                        logger.info(f"Mode changed to: {new_mode}")

                    # Theme toggle
                    elif event.key == pygame.K_t:
                        new_theme = global_state.cycle_theme()
                        logger.info(f"Theme changed to: {new_theme}")

                    # Fullscreen toggle
                    elif event.key == pygame.K_f:
                        self.toggle_fullscreen()

            # Draw
            self.draw_grid()
            pygame.display.flip()

        # Cleanup
        pygame.quit()
        logger.info("MotiBeam Spatial OS Launcher stopped")


def main():
    """Entry point"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    MotiBeam Spatial OS v2.0                          ║
║              Interactive Multi-Realm Computing Platform              ║
╚══════════════════════════════════════════════════════════════════════╝

Controls:
  Navigation:  Arrow Keys / WASD
  Launch:      ENTER / SPACE
  Mode:        M (Normal → Study → Sleep)
  Theme:       T (Neon → Minimal → Night)
  Fullscreen:  F
  Quit:        ESC / Q

Inside Realms:
  Views:       LEFT / RIGHT
  Event:       SPACE
  Exit:        ESC

Starting...
""")

    launcher = SpatialOSLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
