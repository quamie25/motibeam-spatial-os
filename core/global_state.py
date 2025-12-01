"""
MotiBeam Spatial OS - Global State Management

Manages global modes (Normal, Study, Sleep) and themes (Neon, Minimal, Night)
across all realms.
"""

from enum import Enum
from typing import Tuple


class GlobalMode(Enum):
    """Global viewing modes affecting all realms."""
    NORMAL = "normal"
    STUDY = "study"
    SLEEP = "sleep"


class ThemeStyle(Enum):
    """Visual theme styles."""
    NEON = "neon"
    MINIMAL = "minimal"
    NIGHT = "night"


class GlobalState:
    """Global state shared across all realms."""

    def __init__(self):
        self.mode = GlobalMode.NORMAL
        self.theme = ThemeStyle.NEON
        self.fullscreen = True  # Start in fullscreen for projection systems

    def cycle_mode(self):
        """Cycle to next global mode."""
        modes = list(GlobalMode)
        current_index = modes.index(self.mode)
        self.mode = modes[(current_index + 1) % len(modes)]
        print(f"  → Global Mode: {self.mode.value.upper()}")

    def cycle_theme(self):
        """Cycle to next theme."""
        themes = list(ThemeStyle)
        current_index = themes.index(self.theme)
        self.theme = themes[(current_index + 1) % len(themes)]
        print(f"  → Theme: {self.theme.value.upper()}")

    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.fullscreen = not self.fullscreen
        print(f"  → Fullscreen: {'ON' if self.fullscreen else 'OFF'}")

    def get_background_color(self) -> Tuple[int, int, int]:
        """Get background color based on mode and theme."""
        if self.mode == GlobalMode.SLEEP:
            return (5, 5, 10)  # Near black
        elif self.mode == GlobalMode.STUDY:
            if self.theme == ThemeStyle.NEON:
                return (15, 15, 25)  # Dark blue
            elif self.theme == ThemeStyle.MINIMAL:
                return (30, 30, 35)  # Dark gray
            else:  # NIGHT
                return (10, 10, 15)  # Very dark
        else:  # NORMAL
            if self.theme == ThemeStyle.NEON:
                return (10, 10, 20)  # Standard neon dark
            elif self.theme == ThemeStyle.MINIMAL:
                return (25, 25, 30)  # Light gray dark
            else:  # NIGHT
                return (8, 8, 12)  # Dark night

    def get_animation_speed(self) -> float:
        """Get animation speed multiplier based on mode."""
        if self.mode == GlobalMode.SLEEP:
            return 0.2  # Very slow
        elif self.mode == GlobalMode.STUDY:
            return 0.5  # Reduced motion
        else:  # NORMAL
            return 1.0  # Full speed

    def get_brightness_multiplier(self) -> float:
        """Get brightness multiplier for colors."""
        if self.mode == GlobalMode.SLEEP:
            return 0.3  # Very dim
        elif self.mode == GlobalMode.STUDY:
            return 0.7  # Dimmed
        else:  # NORMAL
            return 1.0  # Full brightness

    def should_show_animations(self) -> bool:
        """Check if animations should be shown."""
        return self.mode == GlobalMode.NORMAL
