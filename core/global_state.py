"""
MotiBeam Spatial OS - Global State
Shared state container for all realms
"""


class GlobalState:
    """Global state container for sharing data between realms"""
    def __init__(self):
        self.mode = "NORMAL"  # NORMAL, STUDY, SLEEP
        # Add more shared state attributes as needed


# Create singleton instance
global_state = GlobalState()
