"""
MotiBeam Spatial OS - Base Realm Class
Foundation for all 9 realm implementations
"""

import pygame
import sys
from typing import Tuple

# Add project root to path
sys.path.insert(0, '/home/user/motibeam-spatial-os')

from core.ui.framework import Theme, UIComponents, Animations


class BaseRealm:
    """
    Base class for all MotiBeam Spatial OS realms

    Each realm must:
    - Inherit from BaseRealm
    - Implement update() and render() methods
    - Support ESC key to exit
    - Provide fullscreen pygame experience
    - Cinema-quality visuals with breathing animations
    """

    def __init__(self, realm_id: int, realm_name: str, realm_color: Tuple[int, int, int]):
        """
        Initialize base realm

        Args:
            realm_id: Realm number (1-9)
            realm_name: Display name
            realm_color: Primary RGB color
        """
        self.realm_id = realm_id
        self.realm_name = realm_name
        self.realm_color = realm_color
        self.theme = Theme()

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption(f"MotiBeam Spatial OS - {realm_name}")

        # Clock for smooth 60 FPS
        self.clock = pygame.time.Clock()
        self.running = False
        self.time = 0.0

        # Load fonts (readable from 10-15ft)
        try:
            self.font_huge = pygame.font.Font(None, 180)      # Massive headers
            self.font_large = pygame.font.Font(None, 120)     # Large text
            self.font_medium = pygame.font.Font(None, 80)     # Medium text
            self.font_normal = pygame.font.Font(None, 60)     # Normal text
            self.font_small = pygame.font.Font(None, 45)      # Small text
        except Exception as e:
            print(f"Font loading error: {e}")
            self.font_huge = pygame.font.Font(None, 180)
            self.font_large = pygame.font.Font(None, 120)
            self.font_medium = pygame.font.Font(None, 80)
            self.font_normal = pygame.font.Font(None, 60)
            self.font_small = pygame.font.Font(None, 45)

        # UI Components
        self.ui = UIComponents()
        self.anim = Animations()

    def run(self):
        """Main realm loop"""
        self.running = True

        while self.running:
            dt = self.clock.tick(60) / 1000.0  # 60 FPS, dt in seconds
            self.time += dt

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.running = False
                    else:
                        self.handle_key(event.key)

            # Update and render
            self.update(dt)
            self.render()
            pygame.display.flip()

        pygame.quit()
        return self.realm_id

    def update(self, dt: float):
        """
        Update realm logic (override in subclass)

        Args:
            dt: Delta time in seconds
        """
        pass

    def render(self):
        """
        Render realm visuals (override in subclass)
        """
        # Default: draw background
        self.screen.fill(self.theme.BG_DEEP)

    def handle_key(self, key: int):
        """
        Handle keyboard input (override in subclass for custom controls)

        Args:
            key: pygame key constant
        """
        pass

    def draw_header(self, title: str, subtitle: str = ""):
        """
        Draw realm header with breathing animation

        Args:
            title: Main title text
            subtitle: Optional subtitle text
        """
        # Breathing glow bar
        pulse = self.anim.breathe(self.time, 2.0)
        glow_height = int(8 * pulse)

        for i in range(5):
            alpha = max(0, 80 - i * 15)
            y_offset = 60 - (i * 2)
            color = (*self.realm_color, alpha)
            s = pygame.Surface((self.width, glow_height), pygame.SRCALPHA)
            s.fill(color)
            self.screen.blit(s, (0, y_offset))

        # Main header bar
        pygame.draw.rect(self.screen, self.realm_color, (0, 60, self.width, 5))

        # Title
        self.ui.draw_text_with_shadow(
            self.screen, title, self.font_large,
            (60, 80), self.theme.TEXT_BRIGHT, 4, False
        )

        # Subtitle
        if subtitle:
            self.ui.draw_text_with_shadow(
                self.screen, subtitle, self.font_normal,
                (60, 200), self.theme.TEXT_DIM, 3, False
            )

    def draw_footer(self, controls_text: str = "ESC: Exit"):
        """
        Draw realm footer with controls

        Args:
            controls_text: Control instructions
        """
        # Footer bar
        pygame.draw.rect(self.screen, self.theme.BG_MID,
                        (0, self.height - 80, self.width, 80))

        # Controls text
        self.ui.draw_text_with_shadow(
            self.screen, controls_text, self.font_small,
            (60, self.height - 60), self.theme.TEXT_DIM, 2, False
        )

    def draw_breathing_orb(self, center: Tuple[int, int], base_radius: int,
                          color: Tuple[int, int, int] = None, label: str = ""):
        """
        Draw a breathing orb with optional label

        Args:
            center: (x, y) center position
            base_radius: Base radius
            color: RGB color (uses realm color if None)
            label: Optional label text
        """
        if color is None:
            color = self.realm_color

        self.ui.draw_breathing_circle(self.screen, center, base_radius, color, self.time)

        if label:
            self.ui.draw_text_with_shadow(
                self.screen, label, self.font_medium,
                center, self.theme.TEXT_BRIGHT, 3, True
            )

    def draw_data_panel(self, rect: pygame.Rect, title: str, value: str,
                       unit: str = "", color: Tuple[int, int, int] = None):
        """
        Draw a data display panel

        Args:
            rect: Panel rectangle
            title: Panel title
            value: Main value to display
            unit: Optional unit label
            color: Accent color
        """
        if color is None:
            color = self.realm_color

        # Panel background with glow
        pulse = self.anim.pulse(self.time, 1.5)
        alpha = int(30 * pulse)

        self.ui.draw_gradient_rect(
            self.screen, rect,
            self.theme.BG_MID, self.theme.BG_DARK, alpha
        )

        # Border with breathing effect
        border_width = max(1, int(3 * pulse))
        pygame.draw.rect(self.screen, color, rect, border_width)

        # Title
        title_y = rect.top + 30
        self.ui.draw_text_with_shadow(
            self.screen, title, self.font_normal,
            (rect.centerx, title_y), self.theme.TEXT_DIM, 2, True
        )

        # Value
        value_y = rect.centery + 20
        self.ui.draw_text_with_shadow(
            self.screen, value, self.font_huge,
            (rect.centerx, value_y), color, 4, True
        )

        # Unit
        if unit:
            unit_y = rect.bottom - 60
            self.ui.draw_text_with_shadow(
                self.screen, unit, self.font_medium,
                (rect.centerx, unit_y), self.theme.TEXT_DIM, 2, True
            )
