"""
MotiBeam Spatial OS v0.1 - Main Launcher

3x3 grid launcher for all 9 realms with global mode/theme controls.
"""

import pygame
import sys
from config.theme_neon import NeonTheme
from core.global_state import GlobalState

# Import all realms (will be added incrementally)
REALMS = [
    {"id": "home",      "name": "Home",      "icon": "🏡", "module": "scenes.home_realm",      "class": "HomeRealm"},
    {"id": "clinical",  "name": "Clinical",  "icon": "⚕️", "module": "scenes.clinical_realm",  "class": "ClinicalRealm"},
    {"id": "education", "name": "Education", "icon": "📚", "module": "scenes.education_realm", "class": "EducationRealm"},
    {"id": "transport", "name": "Transport", "icon": "🚗", "module": "scenes.transport_realm", "class": "TransportRealm"},
    {"id": "emergency", "name": "Emergency", "icon": "🚨", "module": "scenes.emergency_realm", "class": "EmergencyRealm"},
    {"id": "security",  "name": "Security",  "icon": "🛡️", "module": "scenes.security_realm",  "class": "SecurityRealm"},
    {"id": "enterprise","name": "Enterprise","icon": "🏢", "module": "scenes.enterprise_realm", "class": "EnterpriseRealm"},
    {"id": "aviation",  "name": "Aviation",  "icon": "✈️", "module": "scenes.aviation_realm",  "class": "AviationRealm"},
    {"id": "maritime",  "name": "Maritime",  "icon": "⚓", "module": "scenes.maritime_realm",  "class": "MaritimeRealm"},
]


class RealmLauncher:
    """Main launcher with 3x3 realm grid."""

    def __init__(self):
        pygame.init()

        # Setup display - get actual screen size and use borderless fullscreen
        info = pygame.display.Info()
        flags = pygame.FULLSCREEN | pygame.NOFRAME
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), flags)
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        pygame.display.set_caption("MotiBeam Spatial OS v0.1")

        # Initialize theme and global state
        self.theme = NeonTheme()
        self.theme.init_fonts()
        self.global_state = GlobalState()

        # Grid state
        self.selected_row = 0
        self.selected_col = 0
        self.grid_cols = 3
        self.grid_rows = 3

        print("\n" + "=" * 70)
        print("  MotiBeam Spatial OS v0.1 - Launcher")
        print("=" * 70)
        print("  Controls:")
        print("    Arrows/WASD: Navigate")
        print("    ENTER/SPACE: Launch realm")
        print("    M: Cycle mode (Normal → Study → Sleep)")
        print("    T: Cycle theme (Neon → Minimal → Night)")
        print("    F: Toggle fullscreen")
        print("    ESC/Q: Quit")
        print("=" * 70)
        print()

    def run(self):
        """Main launcher loop."""
        clock = pygame.time.Clock()
        FPS = 60
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                        running = False

                    elif event.key == pygame.K_m:
                        self.global_state.cycle_mode()

                    elif event.key == pygame.K_t:
                        self.global_state.cycle_theme()

                    elif event.key == pygame.K_f:
                        self.global_state.toggle_fullscreen()
                        info = pygame.display.Info()
                        if self.global_state.fullscreen:
                            flags = pygame.FULLSCREEN | pygame.NOFRAME
                            size = (info.current_w, info.current_h)
                        else:
                            flags = 0
                            size = (int(info.current_w * 0.8), int(info.current_h * 0.8))
                        self.screen = pygame.display.set_mode(size, flags)
                        self.screen_width, self.screen_height = size

                    elif event.key in [pygame.K_UP, pygame.K_w]:
                        self.selected_row = (self.selected_row - 1) % self.grid_rows

                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.selected_row = (self.selected_row + 1) % self.grid_rows

                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.selected_col = (self.selected_col - 1) % self.grid_cols

                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.selected_col = (self.selected_col + 1) % self.grid_cols

                    elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        self.launch_selected_realm()

            # Render
            bg_color = self.global_state.get_background_color()
            self.screen.fill(bg_color)

            self.draw_launcher()

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        print("\n  MotiBeam Spatial OS - Shutdown complete\n")
        sys.exit(0)

    def draw_launcher(self):
        """Draw the 3x3 realm grid."""
        # Title
        brightness = self.global_state.get_brightness_multiplier()
        title_color = tuple(int(c * brightness) for c in self.theme.colors['primary'])

        title = "MOTIBEAM SPATIAL OS"
        title_surf = self.theme.fonts['title'].render(title, True, title_color)
        title_x = (self.screen_width - title_surf.get_width()) // 2
        self.screen.blit(title_surf, (title_x, 80))

        # Subtitle with mode and theme
        subtitle = f"Mode: {self.global_state.mode.value.upper()}  •  Theme: {self.global_state.theme.value.upper()}"
        subtitle_color = tuple(int(c * brightness) for c in self.theme.colors['text_dim'])
        subtitle_surf = self.theme.fonts['label'].render(subtitle, True, subtitle_color)
        subtitle_x = (self.screen_width - subtitle_surf.get_width()) // 2
        self.screen.blit(subtitle_surf, (subtitle_x, 150))

        # 3x3 grid - centered vertically and with more spacing
        tile_width = 480
        tile_height = 240
        gap = 60

        total_grid_width = (tile_width * 3) + (gap * 2)
        total_grid_height = (tile_height * 3) + (gap * 2)

        grid_start_x = (self.screen_width - total_grid_width) // 2
        grid_start_y = 200 + (self.screen_height - 200 - 100 - total_grid_height) // 2

        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                index = row * self.grid_cols + col
                if index < len(REALMS):
                    x = grid_start_x + col * (tile_width + gap)
                    y = grid_start_y + row * (tile_height + gap)

                    is_selected = (row == self.selected_row and col == self.selected_col)
                    self.draw_realm_tile(x, y, tile_width, tile_height, REALMS[index], is_selected)

        # Controls at bottom
        controls = "↑↓←→: Navigate  •  ENTER: Launch  •  M: Mode  •  T: Theme  •  F: Fullscreen  •  ESC: Quit"
        controls_surf = self.theme.fonts['ticker'].render(controls, True, subtitle_color)
        controls_x = (self.screen_width - controls_surf.get_width()) // 2
        self.screen.blit(controls_surf, (controls_x, self.screen_height - 60))

    def draw_realm_tile(self, x: int, y: int, width: int, height: int, realm_info: dict, selected: bool):
        """Draw a single realm tile with enhanced visuals."""
        brightness = self.global_state.get_brightness_multiplier()

        # Border and background - brighter selection
        if selected:
            # Bright glowing selection
            border_color = tuple(min(255, int(c * brightness * 1.5)) for c in self.theme.colors['primary'])
            bg_color = tuple(int(c * brightness * 0.3) for c in self.theme.colors['panel_bg'])
            border_width = 5

            # Draw glow effect for selected tile
            glow_rect = pygame.Rect(x - 4, y - 4, width + 8, height + 8)
            glow_color = tuple(int(c * brightness * 0.4) for c in self.theme.colors['primary'])
            pygame.draw.rect(self.screen, glow_color, glow_rect, 2)
        else:
            border_color = tuple(int(c * brightness * 0.4) for c in self.theme.colors['border'])
            bg_color = tuple(int(c * brightness * 0.08) for c in self.theme.colors['panel_bg'])
            border_width = 2

        tile_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, bg_color, tile_rect)
        pygame.draw.rect(self.screen, border_color, tile_rect, border_width)

        # Icon (larger and centered)
        icon_text = realm_info["icon"]
        try:
            # Use huge font for icons
            icon_font = pygame.font.Font(pygame.font.match_font('monospace', bold=True), 100)
        except:
            icon_font = self.theme.fonts['huge']

        text_color = tuple(int(c * brightness) for c in self.theme.colors['text'])
        icon_surf = icon_font.render(icon_text, True, text_color)
        icon_x = x + (width - icon_surf.get_width()) // 2
        icon_y = y + 50
        self.screen.blit(icon_surf, (icon_x, icon_y))

        # Name (larger font)
        name_surf = self.theme.fonts['panel_title'].render(realm_info["name"], True, text_color)
        name_x = x + (width - name_surf.get_width()) // 2
        name_y = y + height - 50
        self.screen.blit(name_surf, (name_x, name_y))

    def launch_selected_realm(self):
        """Launch the currently selected realm."""
        index = self.selected_row * self.grid_cols + self.selected_col
        if index < len(REALMS):
            realm_info = REALMS[index]

            print(f"\n  ▶ Launching: {realm_info['icon']} {realm_info['name']}")

            try:
                # Dynamically import and instantiate realm
                import importlib
                module = importlib.import_module(realm_info["module"])
                realm_class = getattr(module, realm_info["class"])
                realm = realm_class(self.screen, self.theme, self.global_state)

                # Run realm (blocking)
                continue_running = realm.run()

                if not continue_running:
                    # Realm signaled exit
                    pygame.quit()
                    sys.exit(0)

                print(f"  ← Returned to launcher")

            except ModuleNotFoundError:
                print(f"  ✗ Realm not yet implemented: {realm_info['name']}")
                print(f"    (Module {realm_info['module']} not found)")
            except Exception as e:
                print(f"  ✗ Error launching realm: {e}")
                import traceback
                traceback.print_exc()


def main():
    """Entry point."""
    launcher = RealmLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
