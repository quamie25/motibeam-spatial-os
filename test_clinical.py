#!/usr/bin/env python3
"""
Test script to diagnose Clinical realm import issues
"""

import sys
import os

print("=" * 60)
print("MOTIBEAM CLINICAL REALM DIAGNOSTIC TEST")
print("=" * 60)
print()

# Check Python version
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print()

# Check pygame
try:
    import pygame
    print(f"✓ pygame {pygame.version.ver} installed")
    print(f"  SDL version: {pygame.version.SDL}")
except ImportError as e:
    print(f"✗ pygame NOT installed: {e}")
    print("  Install with: pip3 install pygame")
    sys.exit(1)

print()

# Check project structure
project_root = os.path.dirname(os.path.abspath(__file__))
print(f"Project root: {project_root}")

realms_dir = os.path.join(project_root, 'realms')
clinical_file = os.path.join(realms_dir, 'clinical_health.py')

print(f"Realms directory exists: {os.path.isdir(realms_dir)}")
print(f"Clinical realm file exists: {os.path.isfile(clinical_file)}")
print()

# Add to path if needed
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added to sys.path: {project_root}")
else:
    print(f"Already in sys.path: {project_root}")

print()

# Try importing base realm
try:
    from realms.base_realm import BaseRealm
    print("✓ BaseRealm imported successfully")
except ImportError as e:
    print(f"✗ Failed to import BaseRealm: {e}")
    sys.exit(1)

print()

# Try importing clinical realm
try:
    from realms.clinical_health import ClinicalHealthPro
    print("✓ ClinicalHealthPro imported successfully")
except ImportError as e:
    print(f"✗ Failed to import ClinicalHealthPro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Try creating instance (but don't run it)
try:
    clinical = ClinicalHealthPro()
    print("✓ ClinicalHealthPro instance created successfully")
    print(f"  Realm ID: {clinical.realm_id}")
    print(f"  Realm name: {clinical.realm_name}")
    print(f"  Display size: {clinical.width}x{clinical.height}")

    # Clean up
    pygame.quit()
except Exception as e:
    print(f"✗ Failed to create ClinicalHealthPro instance: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 60)
print("✓ ALL TESTS PASSED - Clinical realm is ready!")
print("=" * 60)
print()
print("Run: python3 spatial_os_ambient.py")
print("Then press '2' to launch Clinical realm")
