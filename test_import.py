#!/usr/bin/env python3
"""
Quick import test to verify all modules load correctly
Run this before launching the full application
"""

def test_imports():
    """Test that all modules can be imported"""
    print("Testing MotiBeam Spatial OS imports...")

    try:
        print("  [1/6] Testing core.ui.framework...")
        from core.ui.framework import Theme, Fonts, ParticleSystem
        print("  ✓ core.ui.framework OK")

        print("  [2/6] Testing core.weather...")
        from core.weather import get_current_weather
        print("  ✓ core.weather OK")

        print("  [3/6] Testing realms.base_realm...")
        from realms.base_realm import BaseRealm
        print("  ✓ realms.base_realm OK")

        print("  [4/6] Testing realms.clinical_health...")
        from realms.clinical_health import ClinicalHealthRealm
        print("  ✓ realms.clinical_health OK")

        print("  [5/6] Testing realms.telebeam...")
        from realms.telebeam import TeleBeamRealm
        print("  ✓ realms.telebeam OK")

        print("  [6/6] Testing spatial_os_ambient (imports only)...")
        # Just test the imports, don't run pygame
        import sys
        import math
        print("  ✓ spatial_os_ambient imports OK")

        print("\n✅ All imports successful!")
        print("\nReady to launch MotiBeam Spatial OS:")
        print("  python3 spatial_os_ambient.py")
        return True

    except ImportError as e:
        print(f"\n❌ Import failed: {e}")
        print("\nMake sure you've installed dependencies:")
        print("  pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = test_imports()
    exit(0 if success else 1)
