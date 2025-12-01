"""
Base Realm Architecture for MotiBeam Spatial OS

All realms inherit from this base class and implement:
- Multiple cycling modes
- Keyboard input handling (SPACE, ESC)
- Consistent layout structure
- Neon theme integration
"""

import pygame
from abc import ABC, abstractmethod
from typing import List, Tuple
import time


class RealmBase(ABC):
    """Abstract base class for all MotiBeam Spatial OS realms."""

    def __init__(self, screen: pygame.Surface, theme):
        """
        Initialize a realm.

        Args:
            screen: Pygame surface to render to
            theme: Theme configuration object
        """
        self.screen = screen
        self.theme = theme
        self.current_mode_index = 0
        self.last_mode_switch_time = time.time()
        self.auto_cycle_interval = 4.0  # seconds
        self.running = True

    @abstractmethod
    def get_modes(self) -> List[str]:
        """Return list of mode names for this realm."""
        pass

    @abstractmethod
    def render_mode(self, mode: str):
        """
        Render the current mode.

        Args:
            mode: The current mode name to render
        """
        pass

    @property
    @abstractmethod
    def realm_name(self) -> str:
        """Return the display name of this realm."""
        pass

    @property
    @abstractmethod
    def realm_key(self) -> str:
        """Return the single-character key identifier (e.g., 'W', 'A', 'M')."""
        pass

    def update(self):
        """Update realm state and handle auto-cycling."""
        current_time = time.time()
        if current_time - self.last_mode_switch_time >= self.auto_cycle_interval:
            self.next_mode()
            self.last_mode_switch_time = current_time

    def render(self):
        """Render the current mode."""
        modes = self.get_modes()
        if modes:
            current_mode = modes[self.current_mode_index]
            self.render_mode(current_mode)

    def next_mode(self):
        """Cycle to the next mode."""
        modes = self.get_modes()
        if modes:
            self.current_mode_index = (self.current_mode_index + 1) % len(modes)
            self.last_mode_switch_time = time.time()

    def handle_input(self, event: pygame.event.Event) -> bool:
        """
        Handle keyboard input.

        Args:
            event: Pygame event

        Returns:
            True if realm should continue running, False to exit
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                return False
            elif event.key == pygame.K_SPACE:
                self.next_mode()
                return True
        return True

    def draw_header(self, title: str, subtitle: str, status: str, status_color: Tuple[int, int, int]):
        """
        Draw the standard header section.

        Args:
            title: Main title text with key prefix (e.g., "[W] ENTERPRISE WORKSPACE")
            subtitle: Subtitle text (e.g., "Operations · Productivity · Team Health")
            status: Status text (e.g., "STABLE", "ACTIVE")
            status_color: RGB color for status indicator
        """
        # Title
        title_surf = self.theme.fonts['title'].render(title, True, self.theme.colors['primary'])
        self.screen.blit(title_surf, (40, 40))

        # Subtitle
        subtitle_surf = self.theme.fonts['subtitle'].render(subtitle, True, self.theme.colors['text_dim'])
        self.screen.blit(subtitle_surf, (40, 90))

        # Status pill
        status_x = self.screen.get_width() - 300
        status_y = 50

        # Draw status indicator circle
        pygame.draw.circle(self.screen, status_color, (status_x, status_y), 8)

        # Draw status text
        status_surf = self.theme.fonts['label'].render(status, True, self.theme.colors['text'])
        self.screen.blit(status_surf, (status_x + 20, status_y - 12))

    def draw_ticker(self, messages: List[str], scroll_offset: float = 0):
        """
        Draw the bottom ticker with scrolling messages.

        Args:
            messages: List of ticker messages
            scroll_offset: Horizontal scroll offset for animation
        """
        ticker_height = 60
        ticker_y = self.screen.get_height() - ticker_height

        # Draw ticker background
        ticker_rect = pygame.Rect(0, ticker_y, self.screen.get_width(), ticker_height)
        pygame.draw.rect(self.screen, self.theme.colors['panel_bg'], ticker_rect)
        pygame.draw.line(self.screen, self.theme.colors['border'],
                        (0, ticker_y), (self.screen.get_width(), ticker_y), 2)

        # Draw ticker messages
        ticker_text = " • ".join(messages)
        ticker_surf = self.theme.fonts['ticker'].render(ticker_text, True, self.theme.colors['text_dim'])
        self.screen.blit(ticker_surf, (20 - scroll_offset % (ticker_surf.get_width() + 100), ticker_y + 20))

    def draw_panel(self, x: int, y: int, width: int, height: int, title: str = None):
        """
        Draw a bordered panel.

        Args:
            x, y: Top-left position
            width, height: Panel dimensions
            title: Optional panel title
        """
        panel_rect = pygame.Rect(x, y, width, height)

        # Draw panel background
        pygame.draw.rect(self.screen, self.theme.colors['panel_bg'], panel_rect)

        # Draw glowing border
        pygame.draw.rect(self.screen, self.theme.colors['border'], panel_rect, 2)

        # Draw title if provided
        if title:
            title_surf = self.theme.fonts['panel_title'].render(title, True, self.theme.colors['accent'])
            self.screen.blit(title_surf, (x + 20, y + 15))

            # Draw title underline
            pygame.draw.line(self.screen, self.theme.colors['border'],
                           (x + 20, y + 50), (x + width - 20, y + 50), 1)

    def draw_big_kpi(self, x: int, y: int, label: str, value: str, color: Tuple[int, int, int] = None):
        """
        Draw a large KPI number with label.

        Args:
            x, y: Position
            label: KPI label
            value: KPI value
            color: Optional color override
        """
        if color is None:
            color = self.theme.colors['primary']

        # Draw value (big)
        value_surf = self.theme.fonts['huge'].render(value, True, color)
        self.screen.blit(value_surf, (x, y))

        # Draw label (smaller, below)
        label_surf = self.theme.fonts['label'].render(label, True, self.theme.colors['text_dim'])
        self.screen.blit(label_surf, (x, y + 90))
