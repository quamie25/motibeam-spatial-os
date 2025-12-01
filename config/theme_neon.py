"""
Neon Theme Configuration for MotiBeam Spatial OS

Provides glowing neon aesthetic with high contrast for readability
from 8-10 feet. All text is large and bold.
"""

import pygame
import math
from typing import Tuple, List


class NeonTheme:
    """Neon theme with glowing effects and large, readable fonts."""

    def __init__(self):
        """Initialize the neon theme."""
        # Color palette - bright neon colors on dark background
        self.colors = {
            # Base colors
            'background': (10, 10, 20),           # Very dark blue-black
            'panel_bg': (15, 15, 30),             # Slightly lighter panel background

            # Neon accent colors
            'primary': (0, 255, 255),              # Cyan - main accent
            'secondary': (255, 0, 255),            # Magenta
            'accent': (0, 255, 128),               # Neon green
            'warning': (255, 255, 0),              # Yellow
            'danger': (255, 50, 50),               # Red
            'success': (0, 255, 100),              # Green

            # Text colors
            'text': (220, 220, 255),               # Light blue-white
            'text_dim': (150, 150, 200),           # Dimmed text
            'text_bright': (255, 255, 255),        # Pure white

            # UI elements
            'border': (0, 200, 255),               # Cyan border
            'border_glow': (0, 150, 255),          # Glowing border
            'highlight': (255, 200, 0),            # Gold highlight
        }

        # Font sizes - large for readability from distance
        self.font_sizes = {
            'huge': 120,        # Massive KPI numbers
            'title': 72,        # Main titles
            'subtitle': 42,     # Subtitles
            'panel_title': 36,  # Panel headers
            'large': 48,        # Large body text
            'medium': 36,       # Medium body text
            'label': 30,        # Labels
            'ticker': 28,       # Ticker text
        }

        # Initialize fonts (will be loaded in init_fonts)
        self.fonts = {}

    def init_fonts(self):
        """Initialize pygame fonts. Call after pygame.init()."""
        # Use monospace font for consistent spacing
        for name, size in self.font_sizes.items():
            self.fonts[name] = pygame.font.Font(pygame.font.match_font('monospace', bold=True), size)

    def draw_glow_circle(self, surface: pygame.Surface, center: Tuple[int, int],
                         radius: int, color: Tuple[int, int, int], glow_layers: int = 3):
        """
        Draw a glowing circle with layered alpha.

        Args:
            surface: Surface to draw on
            center: Circle center (x, y)
            radius: Circle radius
            color: RGB color
            glow_layers: Number of glow layers
        """
        for i in range(glow_layers, 0, -1):
            glow_radius = radius + (i * 4)
            alpha = 100 // (i + 1)

            # Create temporary surface for alpha blending
            glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            glow_color = (*color, alpha)
            pygame.draw.circle(glow_surf, glow_color, (glow_radius, glow_radius), glow_radius)

            surface.blit(glow_surf, (center[0] - glow_radius, center[1] - glow_radius))

        # Draw solid center
        pygame.draw.circle(surface, color, center, radius)

    def draw_glow_rect(self, surface: pygame.Surface, rect: pygame.Rect,
                       color: Tuple[int, int, int], width: int = 2, glow_layers: int = 2):
        """
        Draw a glowing rectangle outline.

        Args:
            surface: Surface to draw on
            rect: Rectangle to draw
            color: RGB color
            width: Border width
            glow_layers: Number of glow layers
        """
        for i in range(glow_layers, 0, -1):
            glow_width = width + (i * 2)
            alpha = 80 // (i + 1)

            # Create temporary surface for alpha blending
            glow_surf = pygame.Surface((rect.width + glow_width * 4, rect.height + glow_width * 4), pygame.SRCALPHA)
            glow_rect = pygame.Rect(glow_width * 2, glow_width * 2, rect.width, rect.height)
            glow_color = (*color, alpha)
            pygame.draw.rect(glow_surf, glow_color, glow_rect, glow_width)

            surface.blit(glow_surf, (rect.x - glow_width * 2, rect.y - glow_width * 2))

        # Draw solid border
        pygame.draw.rect(surface, color, rect, width)

    def draw_radar_rings(self, surface: pygame.Surface, center: Tuple[int, int],
                        max_radius: int, num_rings: int = 5):
        """
        Draw concentric radar rings for aviation/maritime displays.

        Args:
            surface: Surface to draw on
            center: Center point (x, y)
            max_radius: Outer ring radius
            num_rings: Number of rings
        """
        for i in range(1, num_rings + 1):
            radius = (max_radius // num_rings) * i
            alpha = 60 if i % 2 == 0 else 40

            # Create transparent ring
            ring_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            ring_color = (*self.colors['border'], alpha)
            pygame.draw.circle(ring_surf, ring_color, (radius, radius), radius, 2)

            surface.blit(ring_surf, (center[0] - radius, center[1] - radius))

        # Draw crosshairs
        pygame.draw.line(surface, self.colors['border'],
                        (center[0] - max_radius, center[1]),
                        (center[0] + max_radius, center[1]), 1)
        pygame.draw.line(surface, self.colors['border'],
                        (center[0], center[1] - max_radius),
                        (center[0], center[1] + max_radius), 1)

    def draw_background_grid(self, surface: pygame.Surface, grid_size: int = 50):
        """
        Draw subtle background grid pattern.

        Args:
            surface: Surface to draw on
            grid_size: Grid cell size in pixels
        """
        width, height = surface.get_size()
        grid_color = (20, 20, 40)

        # Vertical lines
        for x in range(0, width, grid_size):
            pygame.draw.line(surface, grid_color, (x, 0), (x, height), 1)

        # Horizontal lines
        for y in range(0, height, grid_size):
            pygame.draw.line(surface, grid_color, (0, y), (width, y), 1)

    def draw_neon_circles_background(self, surface: pygame.Surface, frame_count: int = 0):
        """
        Draw animated neon circles background effect.

        Args:
            surface: Surface to draw on
            frame_count: Current frame number for animation
        """
        width, height = surface.get_size()

        # Draw subtle animated circles
        for i in range(5):
            angle = (frame_count + i * 72) % 360
            radius = 150 + i * 50
            x = width // 2 + int(math.cos(math.radians(angle)) * 100)
            y = height // 2 + int(math.sin(math.radians(angle)) * 100)

            # Very transparent circles
            circle_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            color = (*self.colors['border'], 15)
            pygame.draw.circle(circle_surf, color, (radius, radius), radius, 1)

            surface.blit(circle_surf, (x - radius, y - radius))

    def get_status_color(self, status: str) -> Tuple[int, int, int]:
        """
        Get color for a status string.

        Args:
            status: Status name (e.g., 'STABLE', 'ACTIVE', 'WARNING')

        Returns:
            RGB color tuple
        """
        status_upper = status.upper()

        if 'STABLE' in status_upper or 'ACTIVE' in status_upper or 'NORMAL' in status_upper:
            return self.colors['success']
        elif 'WARNING' in status_upper or 'HIGH' in status_upper or 'BUSY' in status_upper:
            return self.colors['warning']
        elif 'CRITICAL' in status_upper or 'ERROR' in status_upper or 'DOWN' in status_upper:
            return self.colors['danger']
        else:
            return self.colors['primary']


# Singleton instance
theme = NeonTheme()


def draw_glow_text(surface: pygame.Surface, font: pygame.font.Font, text: str,
                   pos: Tuple[int, int], color: Tuple[int, int, int],
                   glow_color: Tuple[int, int, int] = None):
    """
    Draw text with a subtle glow effect.

    Args:
        surface: Surface to draw on
        font: Font to use
        text: Text to draw
        pos: Position (x, y)
        color: Text color
        glow_color: Optional glow color (defaults to color)
    """
    if glow_color is None:
        glow_color = color

    # Draw glow layers
    for offset in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
        glow_surf = font.render(text, True, glow_color)
        glow_surf.set_alpha(50)
        surface.blit(glow_surf, (pos[0] + offset[0], pos[1] + offset[1]))

    # Draw main text
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, pos)
