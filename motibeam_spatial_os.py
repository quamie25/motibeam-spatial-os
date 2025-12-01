"""
MotiBeam Spatial OS - Kickstarter Demo
Cinematic multi-realm command wall platform.

Realms:
- Emergency Response
- Security & Surveillance
- Enterprise Workspace
- Aviation Control
- Maritime Operations
"""

import pygame
import sys
import time
from config.theme_neon import NeonTheme
from scenes import (
    EmergencyResponseRealm,
    SecuritySurveillanceRealm,
    EnterpriseWorkspaceRealm,
    AviationControlRealm,
    MaritimeOperationsRealm,
)


def print_banner():
    """Print ASCII art banner."""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║    ███╗   ███╗ ██████╗ ████████╗██╗██████╗ ███████╗ █████╗ ███╗   ███╗")
    print("║    ████╗ ████║██╔═══██╗╚══██╔══╝██║██╔══██╗██╔════╝██╔══██╗████╗ ████║")
    print("║    ██╔████╔██║██║   ██║   ██║   ██║██████╔╝█████╗  ███████║██╔████╔██║")
    print("║    ██║╚██╔╝██║██║   ██║   ██║   ██║██╔══██╗██╔══╝  ██╔══██║██║╚██╔╝██║")
    print("║    ██║ ╚═╝ ██║╚██████╔╝   ██║   ██║██████╔╝███████╗██║  ██║██║ ╚═╝ ██║")
    print("║    ╚═╝     ╚═╝ ╚═════╝    ╚═╝   ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝")
    print("║                                                                      ║")
    print("║                      SPATIAL OS — MOS-1.0                           ║")
    print("║              Multi-Realm Ambient Computing Platform                 ║")
    print("║                        [Kickstarter Demo]                           ║")
    print("║                                                                      ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()


def print_menu():
    """Print realm selection menu."""
    print("=" * 70)
    print("  AVAILABLE REALMS")
    print("=" * 70)
    print("  [1] 🚨  Emergency Response Realm")
    print("  [2] 🛡️  Security & Surveillance Realm")
    print("  [3] 🏢  Enterprise Workspace Realm")
    print("  [4] ✈️  Aviation Control Realm")
    print("  [5] ⚓  Maritime Operations Realm")
    print()
    print("  [A] 🔄  Auto-Loop Demo (All Realms)")
    print("  [Q] 👋  Quit MotiBeam OS")
    print("=" * 70)
    print()


def run_realm(realm, realm_name):
    """
    Run a single realm until completion or ESC.

    Args:
        realm: Cinematic realm instance
        realm_name: Display name for logging
    """
    print(f"\n▶ Starting: {realm_name}")
    print("  Controls: SPACE = Next phase, ESC = Exit")
    print()

    clock = pygame.time.Clock()
    FPS = 60

    while realm.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                realm.running = False
                return False  # Signal to quit entire app
            else:
                if not realm.handle_input(event):
                    return True  # Realm exited normally, return to menu

        realm.update()

        # Clear and render
        realm.screen.fill(realm.theme.colors['background'])
        realm.render()

        pygame.display.flip()
        clock.tick(FPS)

    return True  # Realm completed, return to menu


def run_auto_loop_demo(screen, theme):
    """
    Auto-loop through all realms, showing each for one full cycle.

    Args:
        screen: Pygame surface
        theme: Theme configuration
    """
    print("\n▶ Starting: AUTO-LOOP DEMO")
    print("  All realms will play in sequence...")
    print("  Controls: ESC = Exit to menu")
    print()

    realms = [
        (EmergencyResponseRealm(screen, theme), "Emergency Response"),
        (SecuritySurveillanceRealm(screen, theme), "Security & Surveillance"),
        (EnterpriseWorkspaceRealm(screen, theme), "Enterprise Workspace"),
        (AviationControlRealm(screen, theme), "Aviation Control"),
        (MaritimeOperationsRealm(screen, theme), "Maritime Operations"),
    ]

    clock = pygame.time.Clock()
    FPS = 60

    for realm, realm_name in realms:
        print(f"\n→ Auto-Loop: {realm_name}")

        # Calculate total duration for this realm
        phases = realm.get_phases()
        total_duration = sum(phase.get('duration', 4.5) for phase in phases)

        realm_start = time.time()

        while (time.time() - realm_start) < total_duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print("\n  Auto-loop interrupted by user")
                    return True

            realm.update()

            # Clear and render
            realm.screen.fill(realm.theme.colors['background'])
            realm.render()

            pygame.display.flip()
            clock.tick(FPS)

    print("\n✓ Auto-loop demo complete!")
    time.sleep(1)
    return True


def main():
    """Main entry point with menu system."""
    print_banner()

    # Initialize pygame
    pygame.init()

    # Set up display
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("MotiBeam Spatial OS — Kickstarter Demo")

    # Initialize theme
    theme = NeonTheme()
    theme.init_fonts()

    # Main menu loop
    running = True
    while running:
        print_menu()

        choice = input("  Select option: ").strip().upper()
        print()

        if choice == 'Q':
            print("👋 Shutting down MotiBeam Spatial OS...")
            running = False

        elif choice == 'A':
            # Auto-loop demo
            continue_running = run_auto_loop_demo(screen, theme)
            if not continue_running:
                running = False

        elif choice == '1':
            realm = EmergencyResponseRealm(screen, theme)
            continue_running = run_realm(realm, "🚨 Emergency Response")
            if not continue_running:
                running = False

        elif choice == '2':
            realm = SecuritySurveillanceRealm(screen, theme)
            continue_running = run_realm(realm, "🛡️ Security & Surveillance")
            if not continue_running:
                running = False

        elif choice == '3':
            realm = EnterpriseWorkspaceRealm(screen, theme)
            continue_running = run_realm(realm, "🏢 Enterprise Workspace")
            if not continue_running:
                running = False

        elif choice == '4':
            realm = AviationControlRealm(screen, theme)
            continue_running = run_realm(realm, "✈️ Aviation Control")
            if not continue_running:
                running = False

        elif choice == '5':
            realm = MaritimeOperationsRealm(screen, theme)
            continue_running = run_realm(realm, "⚓ Maritime Operations")
            if not continue_running:
                running = False

        else:
            print("❌ Invalid option. Please select 1-5, A, or Q.")
            time.sleep(1)

    # Cleanup
    pygame.quit()
    print()
    print("=" * 70)
    print("  MotiBeam Spatial OS — Shutdown complete")
    print("=" * 70)
    print()
    sys.exit(0)


if __name__ == "__main__":
    main()
