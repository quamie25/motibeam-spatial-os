"""
Realm Manager for MotiBeam Spatial OS

Manages realm registration, switching, and lifecycle.
"""

import pygame
from typing import Dict, Optional
from core.realm_base import RealmBase


class RealmManager:
    """Manages all realms and handles realm switching."""

    def __init__(self, screen: pygame.Surface, theme):
        """
        Initialize realm manager.

        Args:
            screen: Pygame surface
            theme: Theme configuration
        """
        self.screen = screen
        self.theme = theme
        self.realms: Dict[str, RealmBase] = {}
        self.current_realm: Optional[RealmBase] = None
        self.frame_count = 0

    def register_realm(self, realm: RealmBase):
        """
        Register a realm with the manager.

        Args:
            realm: Realm instance to register
        """
        key = realm.realm_key
        self.realms[key] = realm
        print(f"Registered realm: [{key}] {realm.realm_name}")

    def activate_realm(self, key: str) -> bool:
        """
        Activate a realm by its key.

        Args:
            key: Realm key (e.g., 'W', 'A', 'M')

        Returns:
            True if realm was activated, False if not found
        """
        if key in self.realms:
            self.current_realm = self.realms[key]
            self.current_realm.running = True
            print(f"Activated realm: [{key}] {self.current_realm.realm_name}")
            return True
        return False

    def update(self):
        """Update the current realm."""
        if self.current_realm:
            self.current_realm.update()
        self.frame_count += 1

    def render(self):
        """Render the current realm."""
        # Clear screen with background color
        self.screen.fill(self.theme.colors['background'])

        # Draw background effects
        self.theme.draw_neon_circles_background(self.screen, self.frame_count)

        # Render current realm
        if self.current_realm:
            self.current_realm.render()

        # Draw realm selector hint at top-right (small)
        self.draw_realm_selector_hint()

    def draw_realm_selector_hint(self):
        """Draw small hint showing available realms."""
        hint_x = self.screen.get_width() - 400
        hint_y = 15

        hint_font = pygame.font.Font(pygame.font.match_font('monospace'), 18)

        # Build hint text
        realm_keys = sorted(self.realms.keys())
        hint_parts = []
        for key in realm_keys:
            realm = self.realms[key]
            if realm == self.current_realm:
                hint_parts.append(f"[{key}]")  # Highlight current
            else:
                hint_parts.append(f" {key} ")

        hint_text = "REALMS: " + " ".join(hint_parts)
        hint_surf = hint_font.render(hint_text, True, self.theme.colors['text_dim'])
        self.screen.blit(hint_surf, (hint_x, hint_y))

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events.

        Args:
            event: Pygame event

        Returns:
            True to continue, False to quit
        """
        # Check for realm switching (number keys or letter keys)
        if event.type == pygame.KEYDOWN:
            # Check for realm key shortcuts
            key_char = pygame.key.name(event.key).upper()
            if key_char in self.realms:
                self.activate_realm(key_char)
                return True

        # Pass event to current realm
        if self.current_realm:
            return self.current_realm.handle_input(event)

        return True

    def is_running(self) -> bool:
        """Check if current realm is still running."""
        if self.current_realm:
            return self.current_realm.running
        return True
