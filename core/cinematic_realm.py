"""
Cinematic Realm Base Class for MotiBeam Spatial OS

Phase-based narrative display system for story-driven command walls.
Each realm tells a story through sequential phases with full-screen displays.
"""

import pygame
import time
from typing import List, Dict, Tuple
from abc import ABC, abstractmethod


class CinematicRealm(ABC):
    """Base class for cinematic story-driven realms."""

    def __init__(self, screen: pygame.Surface, theme):
        """
        Initialize cinematic realm.

        Args:
            screen: Pygame surface to render to
            theme: Theme configuration object
        """
        self.screen = screen
        self.theme = theme
        self.current_phase_index = 0
        self.phase_start_time = time.time()
        self.running = True
        self.last_space_press = 0  # For debouncing

    @property
    @abstractmethod
    def realm_name(self) -> str:
        """Return the display name of this realm."""
        pass

    @property
    @abstractmethod
    def realm_key(self) -> str:
        """Return the single-character key identifier."""
        pass

    @property
    @abstractmethod
    def realm_icon(self) -> str:
        """Return the emoji icon for this realm."""
        pass

    @abstractmethod
    def get_phases(self) -> List[Dict]:
        """
        Return list of phase definitions.

        Each phase should be a dict with:
        - title: str (phase title)
        - icon: str (emoji icon)
        - lines: List[str] (content lines)
        - accent: Tuple[int, int, int] (RGB color)
        - duration: float (seconds)
        - ticker: str (optional bottom ticker text)
        """
        pass

    def update(self):
        """Update phase state and handle auto-progression."""
        phases = self.get_phases()
        if not phases:
            return

        current_phase = phases[self.current_phase_index]
        elapsed = time.time() - self.phase_start_time

        # Auto-advance to next phase
        if elapsed >= current_phase.get('duration', 4.0):
            self.next_phase()

    def next_phase(self):
        """Advance to next phase."""
        phases = self.get_phases()
        if phases:
            self.current_phase_index = (self.current_phase_index + 1) % len(phases)
            self.phase_start_time = time.time()

            # Console log
            phase = phases[self.current_phase_index]
            print(f"  → Phase {self.current_phase_index + 1}/{len(phases)}: {phase['title']}")

    def render(self):
        """Render the current phase cinematically."""
        phases = self.get_phases()
        if not phases:
            return

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Get current phase
        current_phase = phases[self.current_phase_index]

        # Draw animated background
        frame_count = int((time.time() - self.phase_start_time) * 30)  # 30 FPS equivalent
        self.theme.draw_neon_circles_background(self.screen, frame_count)

        # Header bar
        self.draw_header_bar(current_phase)

        # Center content - Phase title + icon + lines
        self.draw_phase_content(current_phase, screen_width, screen_height)

        # Bottom ticker
        if 'ticker' in current_phase:
            self.draw_ticker(current_phase['ticker'])

    def draw_header_bar(self, phase: Dict):
        """Draw the top header bar."""
        screen_width = self.screen.get_width()

        # Left: Realm name with key
        realm_title = f"[{self.realm_key}] {self.realm_name}"
        title_surf = self.theme.fonts['subtitle'].render(realm_title, True, self.theme.colors['primary'])
        self.screen.blit(title_surf, (40, 30))

        # Right: Status indicator
        status_x = screen_width - 300
        status_y = 45

        # Pulsing status indicator
        pulse = int(abs((time.time() % 2.0 - 1.0) * 255))
        status_color = (pulse, 255, pulse)

        pygame.draw.circle(self.screen, status_color, (status_x, status_y), 8)

        status_text = "LIVE"
        status_surf = self.theme.fonts['label'].render(status_text, True, self.theme.colors['text'])
        self.screen.blit(status_surf, (status_x + 20, status_y - 12))

    def draw_phase_content(self, phase: Dict, screen_width: int, screen_height: int):
        """Draw the main phase content (title, icon, lines)."""
        # Content area - use 70% of screen width, centered
        content_width = int(screen_width * 0.7)
        content_x = (screen_width - content_width) // 2
        content_y = 200

        # Phase title with icon (huge)
        title_text = f"{phase['icon']}  {phase['title']}"

        # Use huge font for title
        try:
            title_font = self.theme.fonts['huge']
        except KeyError:
            title_font = self.theme.fonts['title']

        title_surf = title_font.render(title_text, True, phase.get('accent', self.theme.colors['primary']))

        # Center the title
        title_x = (screen_width - title_surf.get_width()) // 2
        self.screen.blit(title_surf, (title_x, content_y))

        # Draw accent line under title
        accent_color = phase.get('accent', self.theme.colors['primary'])
        line_y = content_y + title_surf.get_height() + 20
        line_start_x = content_x
        line_end_x = content_x + content_width
        pygame.draw.line(self.screen, accent_color, (line_start_x, line_y), (line_end_x, line_y), 3)

        # Content lines (generous spacing)
        lines_y = line_y + 80
        line_spacing = 70

        for line in phase['lines']:
            line_surf = self.theme.fonts['large'].render(line, True, self.theme.colors['text'])
            self.screen.blit(line_surf, (content_x, lines_y))
            lines_y += line_spacing

    def draw_ticker(self, ticker_text: str):
        """Draw scrolling bottom ticker."""
        ticker_height = 70
        ticker_y = self.screen.get_height() - ticker_height

        # Draw ticker background
        ticker_rect = pygame.Rect(0, ticker_y, self.screen.get_width(), ticker_height)
        pygame.draw.rect(self.screen, self.theme.colors['panel_bg'], ticker_rect)
        pygame.draw.line(self.screen, self.theme.colors['border'],
                        (0, ticker_y), (self.screen.get_width(), ticker_y), 2)

        # Scrolling text
        scroll_offset = (time.time() * 50) % (len(ticker_text) * 15 + self.screen.get_width())
        ticker_surf = self.theme.fonts['ticker'].render(ticker_text, True, self.theme.colors['text_dim'])
        self.screen.blit(ticker_surf, (self.screen.get_width() - scroll_offset, ticker_y + 20))

    def handle_input(self, event: pygame.event.Event) -> bool:
        """
        Handle keyboard input.

        Args:
            event: Pygame event

        Returns:
            True if realm should continue, False to exit
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                return False
            elif event.key == pygame.K_SPACE:
                # Debounce space key (500ms)
                current_time = time.time()
                if current_time - self.last_space_press > 0.5:
                    self.next_phase()
                    self.last_space_press = current_time
                return True
        return True
