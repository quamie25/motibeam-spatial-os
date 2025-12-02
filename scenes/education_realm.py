# scenes/education_realm.py
"""
MotiBeam Spatial OS - Education Realm
Learning and knowledge management
"""

import pygame


class EducationRealm:
    def __init__(self, screen, clock, global_state, standalone=False):
        self.screen = screen
        self.clock = clock
        self.global_state = global_state
        self.standalone = standalone
        self.running = False

    def initialize(self):
        """Initialize the Education Realm"""
        pygame.font.init()
        self.font_title = pygame.font.SysFont("DejaVu Sans", 48, bold=True)
        self.font_body = pygame.font.SysFont("DejaVu Sans", 24)

    def run(self, duration=None):
        """Run the Education Realm"""
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
        """Draw the education realm frame"""
        # Deep purple background
        self.screen.fill((30, 20, 60))

        # Title
        title = self.font_title.render("📚 EDUCATION REALM", True, (220, 200, 255))
        self.screen.blit(title, (50, 50))

        # Mode display
        mode = getattr(self.global_state, "mode", "NORMAL")
        mode_text = self.font_body.render(f"Mode: {mode}", True, (180, 160, 220))
        self.screen.blit(mode_text, (50, 120))

        # Instructions
        instructions = self.font_body.render("Press ESC to exit", True, (150, 130, 200))
        self.screen.blit(instructions, (50, 160))
