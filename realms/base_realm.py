"""
MotiBeam Spatial OS - Base Realm Class
Template for all realm implementations
"""

import pygame
from typing import Optional
from core.ui.framework import Theme, Fonts


class BaseRealm:
    """
    Base class for all MotiBeam realms
    Handles display reuse, event loops, transitions, and FPS control
    """

    def __init__(self, display: pygame.Surface, realm_name: str):
        self.display = display
        self.realm_name = realm_name
        self.width = display.get_width()
        self.height = display.get_height()
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Privacy mode state
        self.privacy_mode = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event
        Returns True if event was handled, False to pass to realm
        """
        if event.type == pygame.KEYDOWN:
            # ESC always exits realm
            if event.key == pygame.K_ESCAPE:
                self.running = False
                return True

            # P toggles privacy mode
            if event.key == pygame.K_p:
                self.privacy_mode = not self.privacy_mode
                return True

        return False

    def update(self):
        """Update realm state - override in subclass"""
        pass

    def draw(self):
        """Draw realm - override in subclass"""
        # Clear screen
        self.display.fill(Theme.BG_DEEP)

        # Draw realm name as placeholder
        font = Fonts.get(Fonts.LARGE, bold=True)
        text_surf = font.render(self.realm_name, True, Theme.WHITE)
        text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2))
        self.display.blit(text_surf, text_rect)

    def run(self):
        """Main realm event loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False  # Signal to quit entire app

                # Let base class handle common events first
                if not self.handle_event(event):
                    # Pass to realm-specific event handler
                    self.on_event(event)

            # Update and draw
            self.update()
            self.draw()

            # Update display
            pygame.display.flip()

            # Maintain FPS
            self.clock.tick(self.fps)

        return True  # Realm exited normally, return to homescreen

    def on_event(self, event: pygame.event.Event):
        """Realm-specific event handling - override in subclass"""
        pass

    def draw_privacy_overlay(self):
        """Draw privacy mode indicator"""
        if self.privacy_mode:
            font = Fonts.get(Fonts.SMALL)
            text_surf = font.render("PRIVACY MODE", True, Theme.AMBER_SOFT)
            text_rect = text_surf.get_rect(topright=(self.width - 30, 30))
            self.display.blit(text_surf, text_rect)

    def blur_sensitive_data(self, text: str) -> str:
        """Replace sensitive data with privacy placeholder"""
        if self.privacy_mode:
            return "••••"
        return text
