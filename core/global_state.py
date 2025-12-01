"""
MotiBeam Spatial OS - Global State Manager
Manages global mode (Normal/Study/Sleep) and theme (Neon/Minimal/Night)
"""


class GlobalState:
    """Singleton global state for MotiBeam Spatial OS"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Mode: affects behavior and visual intensity
        self.mode = "NORMAL"  # NORMAL, STUDY, SLEEP

        # Theme: affects color palette and style
        self.theme = "NEON"  # NEON, MINIMAL, NIGHT

        # Fullscreen state
        self.fullscreen = True

        self._initialized = True

    def cycle_mode(self):
        """Cycle through modes: NORMAL → STUDY → SLEEP → NORMAL"""
        modes = ["NORMAL", "STUDY", "SLEEP"]
        current_idx = modes.index(self.mode)
        self.mode = modes[(current_idx + 1) % len(modes)]
        return self.mode

    def cycle_theme(self):
        """Cycle through themes: NEON → MINIMAL → NIGHT → NEON"""
        themes = ["NEON", "MINIMAL", "NIGHT"]
        current_idx = themes.index(self.theme)
        self.theme = themes[(current_idx + 1) % len(themes)]
        return self.theme

    def get_mode_config(self):
        """Get visual configuration based on current mode"""
        configs = {
            "NORMAL": {
                "background_alpha": 1.0,
                "circle_alpha_multiplier": 1.0,
                "circle_speed_multiplier": 1.0,
                "text_brightness": 1.0,
                "animation_intensity": 1.0
            },
            "STUDY": {
                "background_alpha": 0.7,
                "circle_alpha_multiplier": 0.5,
                "circle_speed_multiplier": 0.6,
                "text_brightness": 0.9,
                "animation_intensity": 0.6
            },
            "SLEEP": {
                "background_alpha": 0.3,
                "circle_alpha_multiplier": 0.2,
                "circle_speed_multiplier": 0.3,
                "text_brightness": 0.5,
                "animation_intensity": 0.3
            }
        }
        return configs[self.mode]

    def get_theme_colors(self):
        """Get color palette based on current theme"""
        themes = {
            "NEON": {
                "bg": (15, 20, 35),
                "primary": (255, 255, 255),
                "secondary": (180, 190, 210),
                "accent_base": (100, 200, 255)
            },
            "MINIMAL": {
                "bg": (20, 20, 25),
                "primary": (240, 240, 240),
                "secondary": (160, 160, 170),
                "accent_base": (120, 180, 220)
            },
            "NIGHT": {
                "bg": (5, 5, 10),
                "primary": (200, 200, 210),
                "secondary": (120, 120, 130),
                "accent_base": (80, 120, 160)
            }
        }
        return themes[self.theme]


# Global instance
global_state = GlobalState()
