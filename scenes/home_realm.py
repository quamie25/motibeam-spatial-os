# scenes/home_realm.py
"""
MotiBeam Spatial OS - Home Realm
Main dashboard and navigation hub
"""

import pygame


class HomeRealm:
    def __init__(self, screen, clock, global_state, standalone=False):
        self.screen = screen
        self.clock = clock
        self.global_state = global_state
        self.standalone = standalone
        self.running = False

    def initialize(self):
        """Initialize the Home Realm"""
        pygame.font.init()
        self.font_title = pygame.font.SysFont("DejaVu Sans", 48, bold=True)
        self.font_body = pygame.font.SysFont("DejaVu Sans", 24)

    def run(self, duration=None):
        """Run the Home Realm"""
        self.initialize()
        self.running = True

        start_ticks = pygame.time.get_ticks()
        max_ms = duration * 1000 if duration else None

        while self.running:
            dt = self.clock.tick(60) / 1000.0
            now_ms = pygame.time.get_ticks()

            if max_ms and (now_ms - start_ticks) >= max_ms:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        break

            self.draw_frame()
            pygame.display.flip()

        if self.standalone:
            pygame.quit()

    def draw_frame(self):
        """Draw the home realm frame"""
        # Dark blue background
        self.screen.fill((10, 20, 50))

        # Title
        title = self.font_title.render("🏡 HOME REALM", True, (200, 220, 255))
        self.screen.blit(title, (50, 50))

        # Mode display
        mode = getattr(self.global_state, "mode", "NORMAL")
        mode_text = self.font_body.render(f"Mode: {mode}", True, (150, 180, 220))
        self.screen.blit(mode_text, (50, 120))

        # Instructions
        instructions = self.font_body.render("Press ESC to exit", True, (120, 150, 200))
        self.screen.blit(instructions, (50, 160))
