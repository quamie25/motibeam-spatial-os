"""
MotiBeam Spatial OS - Spatial Realm Base Class

Base class for all realms with standardized view system, controls, and
global state integration.
"""

import pygame
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from core.global_state import GlobalState


class SpatialRealm(ABC):
    """Base class for all MotiBeam spatial realms."""

    def __init__(self, screen: pygame.Surface, theme, global_state: GlobalState):
        """
        Initialize spatial realm.

        Args:
            screen: Pygame surface
            theme: Theme configuration
            global_state: Global state object
        """
        self.screen = screen
        self.theme = theme
        self.global_state = global_state
        self.current_view_index = 0
        self.running = True
        self.last_interaction_time = time.time()

    @property
    @abstractmethod
    def realm_name(self) -> str:
        """Return realm display name."""
        pass

    @property
    @abstractmethod
    def realm_icon(self) -> str:
        """Return realm emoji icon."""
        pass

    @abstractmethod
    def get_views(self) -> List[Dict]:
        """
        Return list of view definitions.

        Each view should be a dict with:
        - name: str (view name)
        - render: callable (render function)
        """
        pass

    def run(self):
        """Main realm loop with standard controls."""
        clock = pygame.time.Clock()
        FPS = 60

        print(f"\n▶ Running: {self.realm_icon} {self.realm_name}")
        print("  Controls: 1-4 = Views, SPACE = Interact, ESC = Exit")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False  # Signal exit app

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        return True  # Return to launcher

                    elif event.key == pygame.K_SPACE:
                        self.on_interact()

                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        view_num = event.key - pygame.K_1
                        views = self.get_views()
                        if view_num < len(views):
                            self.current_view_index = view_num
                            print(f"  → View {view_num + 1}: {views[view_num]['name']}")

                    elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        self.cycle_view(1 if event.key == pygame.K_RIGHT else -1)

            # Update
            self.update()

            # Render
            bg_color = self.global_state.get_background_color()
            self.screen.fill(bg_color)

            # Draw background effects if animations enabled
            if self.global_state.should_show_animations():
                self.draw_background_effects()

            # Render current view
            self.render_current_view()

            # Draw header and footer
            self.draw_header()
            self.draw_footer()

            pygame.display.flip()
            clock.tick(FPS)

        return True

    def cycle_view(self, direction: int):
        """Cycle to next/previous view."""
        views = self.get_views()
        if views:
            self.current_view_index = (self.current_view_index + direction) % len(views)
            print(f"  → View {self.current_view_index + 1}: {views[self.current_view_index]['name']}")

    def render_current_view(self):
        """Render the currently active view."""
        views = self.get_views()
        if views and self.current_view_index < len(views):
            current_view = views[self.current_view_index]
            render_func = current_view['render']
            render_func()

    def draw_header(self):
        """Draw standard header with realm name and mode."""
        # Realm name and icon
        header_text = f"{self.realm_icon} {self.realm_name}"
        brightness = self.global_state.get_brightness_multiplier()
        color = tuple(int(c * brightness) for c in self.theme.colors['text'])

        header_surf = self.theme.fonts['subtitle'].render(header_text, True, color)
        self.screen.blit(header_surf, (40, 30))

        # Current view indicator
        views = self.get_views()
        if views:
            view_text = f"VIEW {self.current_view_index + 1}/{len(views)}: {views[self.current_view_index]['name'].upper()}"
            view_surf = self.theme.fonts['label'].render(view_text, True, color)
            self.screen.blit(view_surf, (40, 80))

        # Mode indicator (top right)
        mode_text = self.global_state.mode.value.upper()
        mode_color = self.get_mode_color()
        mode_surf = self.theme.fonts['label'].render(mode_text, True, mode_color)
        self.screen.blit(mode_surf, (self.screen.get_width() - 200, 50))

    def draw_footer(self):
        """Draw standard footer with controls."""
        footer_y = self.screen.get_height() - 50
        brightness = self.global_state.get_brightness_multiplier()
        color = tuple(int(c * brightness * 0.6) for c in self.theme.colors['text_dim'])

        controls_text = "1-4: Views • SPACE: Interact • ESC: Exit"
        controls_surf = self.theme.fonts['ticker'].render(controls_text, True, color)
        self.screen.blit(controls_surf, (40, footer_y))

    def draw_background_effects(self):
        """Draw subtle background effects based on theme."""
        if self.global_state.theme.value == "neon":
            frame_count = int(time.time() * 30 * self.global_state.get_animation_speed())
            self.theme.draw_neon_circles_background(self.screen, frame_count)

    def get_mode_color(self) -> Tuple[int, int, int]:
        """Get color for current mode indicator."""
        brightness = self.global_state.get_brightness_multiplier()

        if self.global_state.mode.value == "normal":
            base_color = (0, 255, 200)
        elif self.global_state.mode.value == "study":
            base_color = (255, 200, 100)
        else:  # sleep
            base_color = (150, 150, 200)

        return tuple(int(c * brightness) for c in base_color)

    def update(self):
        """Update realm state. Override in subclasses if needed."""
        pass

    def on_interact(self):
        """Handle SPACE interaction. Override in subclasses."""
        self.last_interaction_time = time.time()
        print(f"  ⚡ Interaction triggered in {self.realm_name}")

    def draw_big_text(self, text: str, y: int, color: Tuple[int, int, int] = None):
        """Draw large centered text."""
        if color is None:
            brightness = self.global_state.get_brightness_multiplier()
            color = tuple(int(c * brightness) for c in self.theme.colors['text'])

        text_surf = self.theme.fonts['title'].render(text, True, color)
        x = (self.screen.get_width() - text_surf.get_width()) // 2
        self.screen.blit(text_surf, (x, y))

    def draw_content_lines(self, lines: List[str], start_y: int, spacing: int = 60):
        """Draw content lines with spacing."""
        brightness = self.global_state.get_brightness_multiplier()
        color = tuple(int(c * brightness) for c in self.theme.colors['text'])

        y = start_y
        for line in lines:
            line_surf = self.theme.fonts['large'].render(line, True, color)
            self.screen.blit(line_surf, (80, y))
            y += spacing

    def draw_panel(self, x: int, y: int, width: int, height: int, title: str = None):
        """Draw a bordered panel."""
        brightness = self.global_state.get_brightness_multiplier()
        border_color = tuple(int(c * brightness) for c in self.theme.colors['border'])
        bg_color = tuple(int(c * brightness * 0.3) for c in self.theme.colors['panel_bg'])

        panel_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, bg_color, panel_rect)
        pygame.draw.rect(self.screen, border_color, panel_rect, 2)

        if title:
            title_color = tuple(int(c * brightness) for c in self.theme.colors['accent'])
            title_surf = self.theme.fonts['panel_title'].render(title, True, title_color)
            self.screen.blit(title_surf, (x + 20, y + 15))
