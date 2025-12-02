"""
MotiBeam Spatial OS - Global State
Shared state container for all realms
"""

import pygame


class GlobalState:
    """Global state container for sharing data between realms"""
    def __init__(self):
        self.mode = "NORMAL"  # NORMAL, STUDY, SLEEP
        self.theme = "NEON"  # NEON, MINIMAL, NIGHT
        # Add more shared state attributes as needed


def get_emoji_font(size=56):
    """
    Attempt to load emoji font, fallback to None if not available.
    Returns None if emoji font cannot be loaded.
    """
    try:
        emoji_font = pygame.font.Font(
            "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", size
        )
        return emoji_font
    except Exception:
        # Emoji font not available
        return None


# Create singleton instance
global_state = GlobalState()
