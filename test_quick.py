#!/usr/bin/env python3
"""
Quick test for Clinical realm on your Raspberry Pi
Run this to see exactly what's happening with imports
"""

print("🔍 Checking Clinical Realm Import...")
print()

import sys
print(f"Python: {sys.version}")
print(f"Executable: {sys.executable}")
print()

# Check pygame
try:
    import pygame
    print(f"✅ pygame {pygame.version.ver} is installed")
except ImportError as e:
    print(f"❌ pygame is NOT installed: {e}")
    print("   Install with: pip3 install pygame")
    sys.exit(1)

print()

# Try importing base realm
try:
    from realms.base_realm import BaseRealm
    print("✅ BaseRealm imports OK")
except ImportError as e:
    print(f"❌ BaseRealm import failed: {e}")
    sys.exit(1)

# Try importing clinical realm
try:
    from realms.clinical_health import ClinicalHealthPro
    print("✅ ClinicalHealthPro imports OK")
    print()
    print("🎉 Everything ready! Press 2 in the homescreen to launch Clinical realm")
except ImportError as e:
    print(f"❌ ClinicalHealthPro import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
