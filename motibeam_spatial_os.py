"""
MotiBeam Spatial OS
Large-format command wall displays for various operational contexts.

Provides neon-themed, high-visibility displays readable from 8-10 feet:
- Enterprise Workspace ("Operations War Room")
- Aviation Control ("ATC Sector Wall")
- Maritime Operations ("Port Command Board")

Controls:
- W: Enterprise Workspace realm
- A: Aviation Control realm
- M: Maritime Operations realm
- SPACE: Cycle to next mode within realm
- ESC: Exit application
"""

import pygame
import sys
from config.theme_neon import NeonTheme
from core.realm_manager import RealmManager
from scenes.enterprise_workspace_realm import EnterpriseWorkspaceRealm
from scenes.aviation_control_realm import AviationControlRealm
from scenes.maritime_operations_realm import MaritimeOperationsRealm


def main():
    """Main entry point for MotiBeam Spatial OS."""
    print("=" * 60)
    print("MotiBeam Spatial OS – Enterprise Command Wall")
    print("=" * 60)
    print()

    # Initialize pygame
    pygame.init()

    # Set up display (full HD for large display readability)
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("MotiBeam Spatial OS")

    # Initialize theme
    theme = NeonTheme()
    theme.init_fonts()

    # Create realm manager
    realm_manager = RealmManager(screen, theme)

    # Register all realms
    print("Registering realms...")
    realm_manager.register_realm(EnterpriseWorkspaceRealm(screen, theme))
    realm_manager.register_realm(AviationControlRealm(screen, theme))
    realm_manager.register_realm(MaritimeOperationsRealm(screen, theme))
    print()

    # Start with Enterprise Workspace realm
    realm_manager.activate_realm('W')
    print()

    # Set up clock for frame rate control
    clock = pygame.time.Clock()
    FPS = 60

    print("MotiBeam Spatial OS running...")
    print()
    print("Controls:")
    print("  W = Enterprise Workspace realm")
    print("  A = Aviation Control realm")
    print("  M = Maritime Operations realm")
    print("  SPACE = Cycle mode within realm")
    print("  ESC = Exit")
    print()

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                # Pass event to realm manager
                if not realm_manager.handle_event(event):
                    running = False

        # Check if current realm is still running
        if not realm_manager.is_running():
            running = False

        # Update
        realm_manager.update()

        # Render
        realm_manager.render()

        # Update display
        pygame.display.flip()

        # Control frame rate
        clock.tick(FPS)

    # Cleanup
    pygame.quit()
    print()
    print("MotiBeam Spatial OS – shutdown complete.")
    sys.exit(0)


if __name__ == "__main__":
    main()
