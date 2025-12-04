"""
MotiBeam Spatial OS - Core UI Framework
Cinema-quality theme system and UI components for ambient computing
"""

import pygame
import math
from typing import Tuple, List
from dataclasses import dataclass

@dataclass
class Theme:
    """Cinema-quality color theme for ambient computing"""

    # Background colors
    BG_DEEP = (8, 12, 20)
    BG_DARK = (15, 20, 30)
    BG_MID = (25, 35, 50)

    # Accent colors
    ACCENT_PRIMARY = (100, 200, 255)
    ACCENT_GLOW = (150, 220, 255)
    ACCENT_DIM = (60, 120, 180)

    # Text colors (readable from 10-15ft)
    TEXT_BRIGHT = (255, 255, 255)
    TEXT_NORMAL = (220, 230, 240)
    TEXT_DIM = (140, 160, 180)
    TEXT_DARK = (80, 100, 120)

    # Realm colors
    REALM_COLORS = {
        1: (100, 200, 255),  # Home & Smart Living
        2: (80, 255, 120),   # Clinical & Health
        3: (200, 100, 255),  # Education & Learning
        4: (255, 255, 100),  # Transport & Automotive
        5: (255, 80, 80),    # Emergency Response
        6: (255, 180, 0),    # Security & Surveillance
        7: (0, 255, 180),    # Enterprise & Workspace
        8: (100, 150, 255),  # Aviation & ATC
        9: (0, 200, 200),    # Maritime & Naval
    }

    # Particle colors
    PARTICLE_COLORS = [
        (100, 200, 255, 30),
        (150, 220, 255, 25),
        (80, 180, 230, 20),
        (120, 210, 255, 35),
    ]

    # Status colors
    STATUS_SUCCESS = (80, 255, 120)
    STATUS_WARNING = (255, 200, 80)
    STATUS_ERROR = (255, 80, 80)
    STATUS_INFO = (100, 200, 255)


class UIComponents:
    """Reusable UI components with cinema-quality rendering"""

    @staticmethod
    def draw_breathing_circle(surface: pygame.Surface, center: Tuple[int, int],
                            base_radius: int, color: Tuple[int, int, int],
                            pulse_time: float, glow: bool = True):
        """Draw a breathing/pulsing circle with optional glow"""
        pulse = math.sin(pulse_time * 2) * 0.15 + 1.0
        radius = int(base_radius * pulse)

        if glow:
            # Multi-layer glow effect
            for i in range(5):
                glow_radius = radius + (i * 10)
                glow_alpha = max(0, 60 - i * 12)
                glow_color = (*color, glow_alpha)
                s = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, glow_color, (glow_radius, glow_radius), glow_radius)
                surface.blit(s, (center[0] - glow_radius, center[1] - glow_radius))

        # Main circle
        pygame.draw.circle(surface, color, center, radius)

    @staticmethod
    def draw_pulsing_ring(surface: pygame.Surface, center: Tuple[int, int],
                         base_radius: int, color: Tuple[int, int, int],
                         pulse_time: float, width: int = 3):
        """Draw a pulsing ring"""
        pulse = math.sin(pulse_time * 3) * 0.1 + 1.0
        radius = int(base_radius * pulse)
        ring_width = max(1, int(width * pulse))
        pygame.draw.circle(surface, color, center, radius, ring_width)

    @staticmethod
    def draw_gradient_rect(surface: pygame.Surface, rect: pygame.Rect,
                          color_top: Tuple[int, int, int],
                          color_bottom: Tuple[int, int, int], alpha: int = 255):
        """Draw a vertical gradient rectangle"""
        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

        for y in range(rect.height):
            ratio = y / rect.height
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            pygame.draw.line(temp_surface, (r, g, b, alpha), (0, y), (rect.width, y))

        surface.blit(temp_surface, rect.topleft)

    @staticmethod
    def draw_text_with_shadow(surface: pygame.Surface, text: str, font: pygame.font.Font,
                            pos: Tuple[int, int], color: Tuple[int, int, int],
                            shadow_offset: int = 3, center: bool = False):
        """Draw text with drop shadow for maximum readability"""
        # Shadow
        shadow_surf = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect()

        if center:
            shadow_rect.center = (pos[0] + shadow_offset, pos[1] + shadow_offset)
        else:
            shadow_rect.topleft = (pos[0] + shadow_offset, pos[1] + shadow_offset)

        surface.blit(shadow_surf, shadow_rect)

        # Main text
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()

        if center:
            text_rect.center = pos
        else:
            text_rect.topleft = pos

        surface.blit(text_surf, text_rect)

        return text_rect

    @staticmethod
    def draw_glowing_line(surface: pygame.Surface, start: Tuple[int, int],
                         end: Tuple[int, int], color: Tuple[int, int, int],
                         width: int = 2, glow_layers: int = 3):
        """Draw a glowing line"""
        for i in range(glow_layers, 0, -1):
            glow_width = width + (i * 4)
            glow_alpha = max(0, 40 - i * 10)
            glow_color = (*color, glow_alpha)
            s = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
            pygame.draw.line(s, glow_color, start, end, glow_width)
            surface.blit(s, (0, 0))

        pygame.draw.line(surface, color, start, end, width)


class Animations:
    """Animation helpers for smooth transitions and effects"""

    @staticmethod
    def ease_in_out(t: float) -> float:
        """Smooth easing function"""
        return t * t * (3.0 - 2.0 * t)

    @staticmethod
    def pulse(t: float, speed: float = 1.0, min_val: float = 0.7, max_val: float = 1.0) -> float:
        """Generate pulsing value"""
        wave = (math.sin(t * speed) + 1) / 2
        return min_val + (max_val - min_val) * wave

    @staticmethod
    def breathe(t: float, speed: float = 2.0) -> float:
        """Generate breathing animation value"""
        return math.sin(t * speed) * 0.15 + 1.0

    @staticmethod
    def wave(t: float, phase: float = 0.0, speed: float = 1.0) -> float:
        """Generate wave animation"""
        return math.sin(t * speed + phase)


class Particle:
    """Ambient particle for living wall effect"""

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 color: Tuple[int, int, int, int], size: int):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = 1.0
        self.max_life = 1.0

    def update(self, dt: float, width: int, height: int):
        """Update particle position and life"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt * 0.2

        # Wrap around screen
        if self.x < 0:
            self.x = width
        elif self.x > width:
            self.x = 0

        if self.y < 0:
            self.y = height
        elif self.y > height:
            self.y = 0

    def draw(self, surface: pygame.Surface):
        """Draw particle with fade"""
        if self.life > 0:
            alpha = int(self.color[3] * self.life)
            color = (*self.color[:3], alpha)
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (self.size, self.size), self.size)
            surface.blit(s, (int(self.x) - self.size, int(self.y) - self.size))

    def is_dead(self) -> bool:
        """Check if particle should be removed"""
        return self.life <= 0
