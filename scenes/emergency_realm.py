# scenes/emergency_realm.py
"""
MotiBeam Spatial OS - Emergency Realm
Emergency response and crisis management
"""

import pygame


class EmergencyRealm:
    def __init__(self, screen, clock, global_state, standalone=False):
        self.screen = screen
        self.clock = clock
        self.global_state = global_state
        self.standalone = standalone
        self.running = False

    def initialize(self):
        """Initialize the Emergency Realm"""
        pygame.font.init()
        self.font_title = pygame.font.SysFont("DejaVu Sans", 48, bold=True)
        self.font_body = pygame.font.SysFont("DejaVu Sans", 24)

    def run(self, duration=None):
        """Run the Emergency Realm"""
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
        """Draw the emergency realm frame"""
        # Dark red background
        self.screen.fill((50, 20, 20))

        # Title
        title = self.font_title.render("🚨 EMERGENCY REALM", True, (255, 180, 180))
        self.screen.blit(title, (50, 50))

        # Mode display
        mode = getattr(self.global_state, "mode", "NORMAL")
        mode_text = self.font_body.render(f"Mode: {mode}", True, (220, 140, 140))
        self.screen.blit(mode_text, (50, 120))

        # Instructions
        instructions = self.font_body.render("Press ESC to exit", True, (190, 120, 120))
        self.screen.blit(instructions, (50, 160))
