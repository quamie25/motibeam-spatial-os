#!/usr/bin/env python3
"""
MotiBeam Spatial OS - Main launcher
Initializes pygame and launches realms
"""

import pygame
import sys
from core.global_state import global_state


class SpatialOSLauncher:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("MotiBeam Spatial OS")
        self.clock = pygame.time.Clock()
        self.global_state = global_state  # Attach global state

    def launch_clinical_realm(self):
        """Launch the Clinical Realm"""
        from scenes.clinical_realm import ClinicalRealm

        print("✓ Launching Clinical Realm...")
        clinical_realm = ClinicalRealm(
            self.screen,
            self.clock,
            global_state=self.global_state,  # Use global_state parameter
            standalone=True
        )
        clinical_realm.run()
        print("✓ Clinical Realm exited cleanly")

    def run(self):
        """Main launcher loop"""
        # For now, directly launch Clinical Realm
        # Later this can be extended to show a realm selector
        self.launch_clinical_realm()

        pygame.quit()
        sys.exit(0)


def main():
    launcher = SpatialOSLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
