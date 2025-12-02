#!/usr/bin/env python3
"""
MotiBeam Spatial OS - Unified Launcher
Initializes pygame and launches realms with shared global state
"""

import pygame
import sys
from core.global_state import global_state
from scenes.home_realm import HomeRealm
from scenes.clinical_realm import ClinicalRealm
from scenes.education_realm import EducationRealm
from scenes.security_realm import SecurityRealm
from scenes.emergency_realm import EmergencyRealm
from scenes.transport_realm import TransportRealm


# Realm registry with factory functions
REALMS = {
    "home": {
        "label": "🏡 Home",
        "factory": lambda screen, clock, gs: HomeRealm(
            screen,
            clock,
            global_state=gs,
            standalone=False,
        ),
    },
    "clinical": {
        "label": "⚕️ Clinical",
        "factory": lambda screen, clock, gs: ClinicalRealm(
            screen,
            clock,
            global_state=gs,
            standalone=False,
        ),
    },
    "education": {
        "label": "📚 Education",
        "factory": lambda screen, clock, gs: EducationRealm(
            screen,
            clock,
            global_state=gs,
            standalone=False,
        ),
    },
    "security": {
        "label": "🔒 Security",
        "factory": lambda screen, clock, gs: SecurityRealm(
            screen,
            clock,
            global_state=gs,
            standalone=False,
        ),
    },
    "emergency": {
        "label": "🚨 Emergency",
        "factory": lambda screen, clock, gs: EmergencyRealm(
            screen,
            clock,
            global_state=gs,
            standalone=False,
        ),
    },
    "transport": {
        "label": "🚗 Transport",
        "factory": lambda screen, clock, gs: TransportRealm(
            screen,
            clock,
            global_state=gs,
            standalone=False,
        ),
    },
}


class SpatialOSLauncher:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("MotiBeam Spatial OS")
        self.clock = pygame.time.Clock()

        # ✅ Attach the global state singleton here
        self.global_state = global_state

        # Launcher UI state
        self.running = False
        self.selected_realm = 0
        self.realm_keys = list(REALMS.keys())

        # Fonts
        pygame.font.init()
        self.font_title = pygame.font.SysFont("DejaVu Sans", 56, bold=True)
        self.font_subtitle = pygame.font.SysFont("DejaVu Sans", 28)
        self.font_realm = pygame.font.SysFont("DejaVu Sans", 32, bold=True)
        self.font_small = pygame.font.SysFont("DejaVu Sans", 20)

    def launch_realm(self, key: str):
        """Launch a specific realm by key"""
        realm_info = REALMS.get(key)
        if not realm_info:
            print(f"ERROR: Unknown realm key: {key}")
            return

        print(f"INFO: Launching realm: {key}")

        factory = realm_info["factory"]
        # Pass global_state to the realm factory
        realm = factory(self.screen, self.clock, self.global_state)

        # All realms expose .run()
        realm.run()

        print(f"INFO: Realm {key} exited")

    def draw_launcher_ui(self):
        """Draw the launcher selection grid"""
        # Dark background
        self.screen.fill((5, 10, 25))

        # Title
        title = self.font_title.render("MOTIBEAM SPATIAL OS", True, (180, 220, 255))
        title_rect = title.get_rect(center=(640, 80))
        self.screen.blit(title, title_rect)

        # Subtitle
        mode = getattr(self.global_state, "mode", "NORMAL")
        subtitle = self.font_subtitle.render(f"Mode: {mode} • Select a Realm", True, (140, 180, 220))
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
            realm_info = REALMS[key]

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
        instructions = "↑↓←→ Navigate  •  ENTER Launch  •  ESC Exit  •  M Toggle Mode"
        instr_surf = self.font_small.render(instructions, True, (120, 160, 200))
        instr_rect = instr_surf.get_rect(center=(640, 680))
        self.screen.blit(instr_surf, instr_rect)

    def handle_input(self, event):
        """Handle launcher input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_RETURN:
                # Launch selected realm
                key = self.realm_keys[self.selected_realm]
                self.launch_realm(key)
            elif event.key == pygame.K_UP:
                self.selected_realm = (self.selected_realm - 2) % len(self.realm_keys)
            elif event.key == pygame.K_DOWN:
                self.selected_realm = (self.selected_realm + 2) % len(self.realm_keys)
            elif event.key == pygame.K_LEFT:
                self.selected_realm = (self.selected_realm - 1) % len(self.realm_keys)
            elif event.key == pygame.K_RIGHT:
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
                print(f"INFO: Mode changed to {self.global_state.mode}")

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

        pygame.quit()
        sys.exit(0)


def main():
    launcher = SpatialOSLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
