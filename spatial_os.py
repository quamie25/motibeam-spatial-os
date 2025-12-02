#!/usr/bin/env python3
"""
MotiBeam Spatial OS - Main launcher
Initializes pygame and launches the Clinical Realm
"""

import pygame
import sys


class GlobalState:
    """Simple global state container for sharing data between realms"""
    def __init__(self):
        self.mode = "NORMAL"  # NORMAL, STUDY, SLEEP


def main():
    # Initialize pygame
    pygame.init()

    # Set up display
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("MotiBeam Spatial OS - Clinical Realm")

    # Create clock for frame rate management
    clock = pygame.time.Clock()

    # Create global state
    global_state = GlobalState()

    # Import and launch Clinical Realm
    from scenes.clinical_realm import ClinicalRealm

    print("✓ Launching Clinical Realm...")
    clinical_realm = ClinicalRealm(screen, clock, global_state, standalone=True)
    clinical_realm.run()

    print("✓ Clinical Realm exited cleanly")
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
