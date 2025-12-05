"""
MotiBeam Spatial OS - Core UI Framework
Projection-friendly, ambient, cinematic interface components
"""

import pygame
import math
import random
from typing import Tuple, List, Optional
from datetime import datetime


# THEME PRESETS - Multiple visual styles
class ThemePreset:
    """Different color themes for homescreen"""

    @staticmethod
    def get_theme(preset_name: str):
        """Get theme by name"""
        themes = {
            "ambient": ThemePreset.ambient(),
            "bright": ThemePreset.bright(),
            "warm": ThemePreset.warm(),
            "cool": ThemePreset.cool(),
        }
        return themes.get(preset_name, themes["ambient"])

    @staticmethod
    def ambient():
        """Ultra-soft ambient theme (default)"""
        return {
            # Background
            "BG_DEEP": (5, 8, 12),
            "BG_DARK": (10, 15, 20),
            "BG_MID": (20, 28, 35),

            # Text - BRIGHTENED for better readability
            "WHITE": (240, 245, 250),         # Brighter white for info
            "GRAY_LIGHT": (200, 205, 215),    # Brighter for readability
            "GRAY_MID": (140, 145, 155),      # Brighter mid gray
            "GRAY_DARK": (70, 75, 85),        # For subtle elements

            # Accent colors
            "BLUE_SOFT": (100, 130, 170),
            "BLUE_GLOW": (110, 140, 180),
            "GREEN_SOFT": (100, 160, 130),
            "AMBER_SOFT": (200, 170, 105),
            "CYAN_SOFT": (100, 160, 180),
        }

    @staticmethod
    def bright():
        """Brighter theme for high ambient light"""
        return {
            "BG_DEEP": (15, 20, 28),
            "BG_DARK": (25, 32, 40),
            "BG_MID": (40, 48, 60),

            "WHITE": (255, 255, 255),
            "GRAY_LIGHT": (220, 225, 235),
            "GRAY_MID": (180, 185, 195),
            "GRAY_DARK": (120, 125, 135),

            "BLUE_SOFT": (120, 160, 220),
            "BLUE_GLOW": (140, 180, 240),
            "GREEN_SOFT": (120, 200, 160),
            "AMBER_SOFT": (240, 200, 120),
            "CYAN_SOFT": (120, 200, 220),
        }

    @staticmethod
    def warm():
        """Warm amber/orange tones"""
        return {
            "BG_DEEP": (12, 8, 5),
            "BG_DARK": (20, 15, 10),
            "BG_MID": (35, 28, 20),

            "WHITE": (250, 240, 230),
            "GRAY_LIGHT": (220, 200, 180),
            "GRAY_MID": (160, 140, 120),
            "GRAY_DARK": (80, 70, 60),

            "BLUE_SOFT": (140, 120, 100),
            "BLUE_GLOW": (160, 140, 120),
            "GREEN_SOFT": (140, 160, 100),
            "AMBER_SOFT": (220, 180, 100),
            "CYAN_SOFT": (140, 150, 120),
        }

    @staticmethod
    def cool():
        """Cool blue/cyan tones"""
        return {
            "BG_DEEP": (5, 10, 15),
            "BG_DARK": (10, 18, 25),
            "BG_MID": (20, 32, 42),

            "WHITE": (230, 240, 250),
            "GRAY_LIGHT": (180, 200, 220),
            "GRAY_MID": (120, 140, 160),
            "GRAY_DARK": (60, 75, 90),

            "BLUE_SOFT": (80, 130, 180),
            "BLUE_GLOW": (100, 150, 200),
            "GREEN_SOFT": (80, 160, 150),
            "AMBER_SOFT": (150, 170, 180),
            "CYAN_SOFT": (80, 170, 200),
        }


# ACTIVE THEME (can be swapped at runtime)
class Theme:
    """Projection-friendly color palette - soft, readable from 10-15ft"""

    # Current theme name
    current_theme = "ambient"

    @classmethod
    def load_theme(cls, preset_name: str):
        """Load a theme preset"""
        cls.current_theme = preset_name
        theme_data = ThemePreset.get_theme(preset_name)

        # Background
        cls.BG_DEEP = theme_data["BG_DEEP"]
        cls.BG_DARK = theme_data["BG_DARK"]
        cls.BG_MID = theme_data["BG_MID"]

        # Text colors
        cls.WHITE = theme_data["WHITE"]
        cls.GRAY_LIGHT = theme_data["GRAY_LIGHT"]
        cls.GRAY_MID = theme_data["GRAY_MID"]
        cls.GRAY_DARK = theme_data["GRAY_DARK"]

        # Accent colors
        cls.BLUE_SOFT = theme_data["BLUE_SOFT"]
        cls.BLUE_GLOW = theme_data["BLUE_GLOW"]
        cls.GREEN_SOFT = theme_data["GREEN_SOFT"]
        cls.AMBER_SOFT = theme_data["AMBER_SOFT"]
        cls.CYAN_SOFT = theme_data["CYAN_SOFT"]
        cls.RED_SOFT = (180, 100, 100)
        cls.PURPLE_SOFT = (150, 120, 170)

    # Background (darker for better contrast)
    BG_DEEP = (5, 8, 12)
    BG_DARK = (10, 15, 20)
    BG_MID = (20, 28, 35)

    # Text colors - BRIGHTENED for information
    WHITE = (240, 245, 250)          # Brighter for readability
    GRAY_LIGHT = (200, 205, 215)     # Brighter light gray
    GRAY_MID = (140, 145, 155)       # Brighter mid gray
    GRAY_DARK = (70, 75, 85)         # For subtle elements

    # Ultra-soft accent colors (VERY muted, cinematic)
    BLUE_SOFT = (100, 130, 170)      # Slightly brighter
    BLUE_GLOW = (110, 140, 180)      # Slightly brighter
    GREEN_SOFT = (100, 160, 130)     # Softer green
    AMBER_SOFT = (200, 170, 105)     # Muted amber
    RED_SOFT = (180, 100, 100)       # Softer red
    PURPLE_SOFT = (150, 120, 170)    # Dimmer purple
    CYAN_SOFT = (100, 160, 180)      # Muted cyan

    # Clinical/Health colors (softer for ambient)
    HEALTH_HR = (180, 90, 105)       # Softer heart rate red
    HEALTH_BP = (85, 115, 180)       # Softer blood pressure blue
    HEALTH_O2 = (85, 145, 115)       # Softer oxygen green
    HEALTH_TEMP = (180, 135, 85)     # Softer temperature amber

    # Status colors (muted)
    STATUS_SUCCESS = (85, 145, 115)
    STATUS_WARNING = (180, 150, 85)
    STATUS_ERROR = (160, 85, 85)
    STATUS_INFO = (85, 115, 160)

    # TeleBeam colors (softer)
    TELEBEAM_TRUSTED = (85, 145, 115)     # Known contact - soft green
    TELEBEAM_UNKNOWN = (180, 150, 85)     # Unknown - soft yellow
    TELEBEAM_SPAM = (160, 85, 85)         # Likely spam - soft red
    TELEBEAM_EMERGENCY = (180, 90, 90)    # Emergency - softer red

    # Transparency levels (reduced for softer appearance)
    ALPHA_SUBTLE = 25         # Very subtle
    ALPHA_MEDIUM = 70         # Medium (reduced from 100)
    ALPHA_VISIBLE = 120       # Visible (reduced from 160)
    ALPHA_SOLID = 255


class Fonts:
    """Font management - large, readable sizes only"""

    _fonts = {}

    @classmethod
    def get(cls, size: int, bold: bool = False) -> pygame.font.Font:
        """Get or create font - caching for performance"""
        key = (size, bold)
        if key not in cls._fonts:
            try:
                # Try to use a clean sans-serif font
                font_name = pygame.font.match_font('arial', bold=bold)
                if font_name:
                    cls._fonts[key] = pygame.font.Font(font_name, size)
                else:
                    cls._fonts[key] = pygame.font.SysFont('arial', size, bold=bold)
            except:
                cls._fonts[key] = pygame.font.Font(None, size)
        return cls._fonts[key]

    # Standard sizes (all large for projection)
    GIANT = 120      # Realm titles, major headings
    HUGE = 96        # Vitals numbers
    LARGE = 72       # Realm names, important info
    MEDIUM = 56      # Secondary info
    NORMAL = 48      # Body text, ticker
    SMALL = 36       # Smallest allowed (still readable from distance)


def draw_text_shadowed(surface: pygame.Surface, text: str, pos: Tuple[int, int],
                       font: pygame.font.Font, color: Tuple[int, int, int],
                       shadow_offset: int = 3, center: bool = False):
    """Draw text with subtle shadow for depth"""
    # Shadow
    shadow_surf = font.render(text, True, (0, 0, 0))
    shadow_rect = shadow_surf.get_rect()

    # Text
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()

    if center:
        shadow_rect.center = (pos[0] + shadow_offset, pos[1] + shadow_offset)
        text_rect.center = pos
    else:
        shadow_rect.topleft = (pos[0] + shadow_offset, pos[1] + shadow_offset)
        text_rect.topleft = pos

    surface.blit(shadow_surf, shadow_rect)
    surface.blit(text_surf, text_rect)

    return text_rect


def draw_glow_circle(surface: pygame.Surface, pos: Tuple[int, int],
                     radius: int, color: Tuple[int, int, int],
                     intensity: float = 1.0):
    """Draw soft glowing circle - ambient, not harsh"""
    glow_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)

    # Multiple layers for soft glow
    layers = 5
    for i in range(layers):
        alpha = int((Theme.ALPHA_SUBTLE / layers) * intensity * (layers - i))
        r = radius + (i * radius // 2)
        pygame.draw.circle(glow_surf, (*color, alpha),
                          (radius * 2, radius * 2), r)

    # Core circle
    pygame.draw.circle(glow_surf, color, (radius * 2, radius * 2), radius)

    blit_pos = (pos[0] - radius * 2, pos[1] - radius * 2)
    surface.blit(glow_surf, blit_pos)


def draw_glow_rect(surface: pygame.Surface, rect: pygame.Rect,
                   color: Tuple[int, int, int], glow_size: int = 20,
                   alpha: int = Theme.ALPHA_MEDIUM):
    """Draw rectangle with soft glow border"""
    glow_surf = pygame.Surface((rect.width + glow_size * 2,
                                rect.height + glow_size * 2), pygame.SRCALPHA)

    # Glow layers
    layers = 3
    for i in range(layers):
        layer_alpha = alpha // (layers - i + 1)
        offset = glow_size - (i * glow_size // layers)
        layer_rect = pygame.Rect(glow_size - offset, glow_size - offset,
                                rect.width + offset * 2, rect.height + offset * 2)
        pygame.draw.rect(glow_surf, (*color, layer_alpha), layer_rect, border_radius=15)

    # Core rectangle
    core_rect = pygame.Rect(glow_size, glow_size, rect.width, rect.height)
    pygame.draw.rect(glow_surf, color, core_rect, border_radius=12)

    blit_pos = (rect.x - glow_size, rect.y - glow_size)
    surface.blit(glow_surf, blit_pos)


class BreathingAnimation:
    """Smooth breathing effect for ambient elements"""

    def __init__(self, min_val: float = 0.6, max_val: float = 1.0,
                 speed: float = 0.02):
        self.min_val = min_val
        self.max_val = max_val
        self.speed = speed
        self.phase = 0

    def update(self):
        """Update animation phase"""
        self.phase += self.speed
        if self.phase > math.pi * 2:
            self.phase -= math.pi * 2

    def get_value(self) -> float:
        """Get current breath value (oscillates smoothly)"""
        normalized = (math.sin(self.phase) + 1) / 2  # 0 to 1
        return self.min_val + (normalized * (self.max_val - self.min_val))


class PulseAnimation:
    """Quick pulse effect for notifications"""

    def __init__(self, duration: int = 30):
        self.duration = duration
        self.frame = 0
        self.active = False

    def trigger(self):
        """Start pulse"""
        self.frame = 0
        self.active = True

    def update(self):
        """Update pulse animation"""
        if self.active:
            self.frame += 1
            if self.frame >= self.duration:
                self.active = False

    def get_intensity(self) -> float:
        """Get current pulse intensity (0 to 1)"""
        if not self.active:
            return 0
        # Ease out
        progress = self.frame / self.duration
        return 1.0 - (progress * progress)


class Particle:
    """Single particle for ambient background"""

    def __init__(self, x: float, y: float, size: float,
                 velocity: Tuple[float, float], color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.size = size
        self.vx, self.vy = velocity
        self.color = color
        self.life = 1.0
        self.decay = random.uniform(0.001, 0.003)

    def update(self, width: int, height: int):
        """Update particle position and life"""
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay

        # Wrap around screen
        if self.x < 0:
            self.x = width
        elif self.x > width:
            self.x = 0
        if self.y < 0:
            self.y = height
        elif self.y > height:
            self.y = 0

    def is_dead(self) -> bool:
        return self.life <= 0

    def draw(self, surface: pygame.Surface):
        """Draw particle with fade"""
        alpha = int(self.life * Theme.ALPHA_SUBTLE)
        if alpha > 0:
            size = int(self.size * self.life)
            if size > 0:
                particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surf, (*self.color, alpha),
                                 (size, size), size)
                surface.blit(particle_surf, (int(self.x) - size, int(self.y) - size))


class ParticleSystem:
    """Ambient particle system - living wall background"""

    def __init__(self, width: int, height: int, max_particles: int = 100):
        self.width = width
        self.height = height
        self.max_particles = max_particles
        self.particles: List[Particle] = []
        self.spawn_timer = 0
        self.spawn_rate = 5  # Frames between spawns

    def spawn_particle(self):
        """Create new particle"""
        x = random.uniform(0, self.width)
        y = random.uniform(0, self.height)
        size = random.uniform(1, 4)

        # Slow, gentle movement
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(0.1, 0.5)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed

        # Soft blue/purple/cyan colors
        color_choice = random.choice([
            Theme.BLUE_SOFT,
            Theme.PURPLE_SOFT,
            Theme.CYAN_SOFT
        ])

        self.particles.append(Particle(x, y, size, (vx, vy), color_choice))

    def update(self):
        """Update all particles"""
        # Remove dead particles
        self.particles = [p for p in self.particles if not p.is_dead()]

        # Update existing
        for particle in self.particles:
            particle.update(self.width, self.height)

        # Spawn new
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_rate and len(self.particles) < self.max_particles:
            self.spawn_particle()
            self.spawn_timer = 0

    def draw(self, surface: pygame.Surface):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(surface)


class Sparkline:
    """Mini graph for vitals display"""

    def __init__(self, width: int, height: int, max_points: int = 50):
        self.width = width
        self.height = height
        self.max_points = max_points
        self.points: List[float] = []

    def add_value(self, value: float):
        """Add value (0.0 to 1.0 range)"""
        self.points.append(value)
        if len(self.points) > self.max_points:
            self.points.pop(0)

    def draw(self, surface: pygame.Surface, pos: Tuple[int, int],
             color: Tuple[int, int, int], line_width: int = 3):
        """Draw sparkline graph"""
        if len(self.points) < 2:
            return

        step = self.width / (self.max_points - 1)

        points = []
        for i, value in enumerate(self.points):
            x = pos[0] + (i * step)
            y = pos[1] + self.height - (value * self.height)
            points.append((x, y))

        # Draw line with glow
        if len(points) >= 2:
            # Glow layer
            glow_surf = pygame.Surface((self.width + 20, self.height + 20),
                                       pygame.SRCALPHA)
            glow_points = [(p[0] - pos[0] + 10, p[1] - pos[1] + 10) for p in points]
            pygame.draw.lines(glow_surf, (*color, Theme.ALPHA_MEDIUM),
                            False, glow_points, line_width + 4)
            surface.blit(glow_surf, (pos[0] - 10, pos[1] - 10))

            # Core line
            pygame.draw.lines(surface, color, False, points, line_width)


class ECGWaveform:
    """Realistic ECG waveform generator (P-QRS-T complex)"""

    def __init__(self, width: int, height: int, bpm: int = 72):
        self.width = width
        self.height = height
        self.bpm = bpm
        self.phase = 0
        self.speed = (bpm / 60.0) * 0.05  # Animation speed

    def get_waveform_value(self, x: float) -> float:
        """Generate realistic ECG shape (0.0 to 1.0)"""
        # P-QRS-T complex simulation
        x = x % 1.0

        baseline = 0.4

        # P wave (0.0 - 0.2)
        if x < 0.15:
            p_val = math.sin(x * math.pi / 0.15) * 0.08
            return baseline + p_val

        # PR segment (0.15 - 0.25)
        elif x < 0.25:
            return baseline

        # QRS complex (0.25 - 0.35)
        elif x < 0.35:
            qrs_x = (x - 0.25) / 0.1
            if qrs_x < 0.3:  # Q dip
                return baseline - 0.05
            elif qrs_x < 0.6:  # R spike
                return baseline + ((qrs_x - 0.3) / 0.3) * 0.5
            else:  # S dip
                return baseline - ((qrs_x - 0.6) / 0.4) * 0.08

        # ST segment (0.35 - 0.45)
        elif x < 0.45:
            return baseline

        # T wave (0.45 - 0.7)
        elif x < 0.7:
            t_x = (x - 0.45) / 0.25
            t_val = math.sin(t_x * math.pi) * 0.15
            return baseline + t_val

        # Baseline (0.7 - 1.0)
        else:
            return baseline

    def update(self):
        """Update animation phase"""
        self.phase += self.speed
        if self.phase > 1.0:
            self.phase -= 1.0

    def draw(self, surface: pygame.Surface, pos: Tuple[int, int],
             color: Tuple[int, int, int], line_width: int = 3):
        """Draw ECG waveform"""
        points = []
        num_points = 200

        for i in range(num_points):
            x_norm = (i / num_points) + self.phase
            y_val = self.get_waveform_value(x_norm)

            x = pos[0] + (i * self.width / num_points)
            y = pos[1] + self.height - (y_val * self.height)
            points.append((x, y))

        if len(points) >= 2:
            # Glow layer
            glow_surf = pygame.Surface((self.width + 20, self.height + 20),
                                       pygame.SRCALPHA)
            glow_points = [(p[0] - pos[0] + 10, p[1] - pos[1] + 10) for p in points]
            pygame.draw.lines(glow_surf, (*color, Theme.ALPHA_MEDIUM),
                            False, glow_points, line_width + 4)
            surface.blit(glow_surf, (pos[0] - 10, pos[1] - 10))

            # Core line
            pygame.draw.lines(surface, color, False, points, line_width)


class ScrollingTicker:
    """Horizontal scrolling text ticker - large and readable"""

    def __init__(self, width: int, messages: List[str], font_size: int = Fonts.NORMAL):
        self.width = width
        self.messages = messages
        self.font = Fonts.get(font_size, bold=False)
        self.scroll_x = width
        self.scroll_speed = 2

        # Pre-render message text
        self.message_text = "   •   ".join(messages)
        self.text_surf = self.font.render(self.message_text, True, Theme.WHITE)
        self.text_width = self.text_surf.get_width()

    def update(self):
        """Update scroll position"""
        self.scroll_x -= self.scroll_speed

        # Loop when text scrolls off
        if self.scroll_x < -self.text_width:
            self.scroll_x = self.width

    def draw(self, surface: pygame.Surface, y: int):
        """Draw scrolling ticker"""
        # Draw text (may need to draw twice for seamless loop)
        surface.blit(self.text_surf, (self.scroll_x, y))

        # Draw second copy if first is scrolling off
        if self.scroll_x < 0:
            surface.blit(self.text_surf, (self.scroll_x + self.text_width + 50, y))


def format_time() -> str:
    """Get formatted current time"""
    return datetime.now().strftime("%I:%M %p")


def format_date() -> str:
    """Get formatted current date"""
    return datetime.now().strftime("%A, %B %d, %Y")
