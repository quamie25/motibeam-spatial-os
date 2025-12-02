#!/usr/bin/env python3
"""
MotiBeam Spatial OS - Unified Launcher
Initializes pygame and launches realms with shared global state
"""

import pygame
import sys
import logging
import importlib
from core.global_state import global_state, get_emoji_font
from config.realms_config import REALMS_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)


class SpatialOSLauncher:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("MotiBeam Spatial OS v2.0")

        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        # IMPORTANT: shared state for all realms
        self.global_state = global_state

        # Launcher UI state
        self.running = False
        self.selected_realm = 0
        self.realm_keys = list(REALMS_CONFIG.keys())

        # Fonts
        pygame.font.init()
        self.font_title = pygame.font.SysFont("DejaVu Sans", 56, bold=True)
        self.font_subtitle = pygame.font.SysFont("DejaVu Sans", 28)
        self.font_realm = pygame.font.SysFont("DejaVu Sans", 32, bold=True)
        self.font_small = pygame.font.SysFont("DejaVu Sans", 20)

        # Try to load emoji font
        self.emoji_font = get_emoji_font()

        logging.info("MotiBeam Spatial OS Launcher starting...")
        logging.info(f"Mode: {self.global_state.mode}, Theme: {self.global_state.theme}")

    def launch_realm(self, realm_key: str):
        """Launch a specific realm by key using dynamic import"""
        cfg = REALMS_CONFIG.get(realm_key)
        if not cfg:
            logging.error(f"Unknown realm: {realm_key}")
            return

        logging.info(f"Launching realm: {realm_key}")

        try:
            # Dynamically import the realm module and class
            module = importlib.import_module(cfg["module"])
            realm_class = getattr(module, cfg["class_name"])

            # Instantiate the realm with shared global state
            realm = realm_class(
                screen=self.screen,
                clock=self.clock,
                global_state=self.global_state,
                standalone=False,
            )

            # Run the realm
            realm.run()

            logging.info(f"Realm {realm_key} exited cleanly")

        except Exception as e:
            logging.exception(f"Failed to load realm {realm_key}: {e}")

    def draw_launcher_ui(self):
        """Draw the launcher selection grid"""
        # Dark background
        self.screen.fill((5, 10, 25))

        # Title
        title = self.font_title.render("MOTIBEAM SPATIAL OS", True, (180, 220, 255))
        title_rect = title.get_rect(center=(640, 80))
        self.screen.blit(title, title_rect)

        # Subtitle with mode and theme
        mode = getattr(self.global_state, "mode", "NORMAL")
        theme = getattr(self.global_state, "theme", "NEON")
        subtitle = self.font_subtitle.render(
            f"Mode: {mode} • Theme: {theme} • Select a Realm",
            True,
            (140, 180, 220)
        )
        subtitle_rect = subtitle.get_rect(center=(640, 130))
        self.screen.blit(subtitle, subtitle_rect)

        # Grid of realms (2 columns, 3 rows)
        grid_cols = 2
        grid_rows = 3
        card_width = 480
        card_height = 120
        gap_x = 40
        gap_y = 30
        start_x = (1280 - (grid_cols * card_width + (grid_cols - 1) * gap_x)) // 2
        start_y = 200

        for idx, key in enumerate(self.realm_keys):
            realm_info = REALMS_CONFIG[key]

            row = idx // grid_cols
            col = idx % grid_cols

            x = start_x + col * (card_width + gap_x)
            y = start_y + row * (card_height + gap_y)

            # Card background
            is_selected = (idx == self.selected_realm)
            bg_color = (40, 80, 120) if is_selected else (20, 40, 60)
            border_color = (100, 180, 255) if is_selected else (60, 100, 140)

            pygame.draw.rect(
                self.screen,
                bg_color,
                (x, y, card_width, card_height),
                border_radius=10
            )
            pygame.draw.rect(
                self.screen,
                border_color,
                (x, y, card_width, card_height),
                width=3,
                border_radius=10
            )

            # Realm label
            label_text = realm_info["label"]
            label_color = (220, 240, 255) if is_selected else (160, 200, 230)
            label = self.font_realm.render(label_text, True, label_color)
            label_rect = label.get_rect(center=(x + card_width // 2, y + card_height // 2))
            self.screen.blit(label, label_rect)

        # Instructions
        instructions = "↑↓←→ Navigate  •  ENTER Launch  •  M Mode  •  T Theme  •  ESC Exit"
        instr_surf = self.font_small.render(instructions, True, (120, 160, 200))
        instr_rect = instr_surf.get_rect(center=(640, 680))
        self.screen.blit(instr_surf, instr_rect)

    def handle_input(self, event):
        """Handle launcher input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                self.running = False
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Launch selected realm
                key = self.realm_keys[self.selected_realm]
                self.launch_realm(key)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_realm = (self.selected_realm - 2) % len(self.realm_keys)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_realm = (self.selected_realm + 2) % len(self.realm_keys)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.selected_realm = (self.selected_realm - 1) % len(self.realm_keys)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.selected_realm = (self.selected_realm + 1) % len(self.realm_keys)
            elif event.key == pygame.K_m:
                # Toggle mode (NORMAL -> STUDY -> SLEEP -> NORMAL)
                current_mode = getattr(self.global_state, "mode", "NORMAL")
                if current_mode == "NORMAL":
                    self.global_state.mode = "STUDY"
                elif current_mode == "STUDY":
                    self.global_state.mode = "SLEEP"
                else:
                    self.global_state.mode = "NORMAL"
                logging.info(f"Mode changed to {self.global_state.mode}")
            elif event.key == pygame.K_t:
                # Toggle theme (NEON -> MINIMAL -> NIGHT -> NEON)
                current_theme = getattr(self.global_state, "theme", "NEON")
                if current_theme == "NEON":
                    self.global_state.theme = "MINIMAL"
                elif current_theme == "MINIMAL":
                    self.global_state.theme = "NIGHT"
                else:
                    self.global_state.theme = "NEON"
                logging.info(f"Theme changed to {self.global_state.theme}")

    def run(self):
        """Main launcher loop"""
        self.running = True

        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                self.handle_input(event)

            self.draw_launcher_ui()
            pygame.display.flip()

        logging.info("Launcher exiting...")
        pygame.quit()
        sys.exit(0)


def main():
    launcher = SpatialOSLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
