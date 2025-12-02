#!/usr/bin/env python3
"""
Diagnostic script to check SpatialOSLauncher global_state setup
"""

import sys
import os

print("=" * 70)
print("MotiBeam Spatial OS - Diagnostic Check")
print("=" * 70)

# Check current directory
print(f"\n1. Current directory: {os.getcwd()}")

# Check if spatial_os.py exists
spatial_os_path = "spatial_os.py"
if os.path.exists(spatial_os_path):
    print(f"2. File exists: {spatial_os_path}")

    # Read and check for global_state assignment
    with open(spatial_os_path, 'r') as f:
        content = f.read()

    # Check for import
    if "from core.global_state import global_state" in content:
        print("   ✓ Has correct import: from core.global_state import global_state")
    else:
        print("   ✗ Missing import: from core.global_state import global_state")

    # Check for self.global_state assignment
    if "self.global_state = global_state" in content:
        print("   ✓ Has self.global_state = global_state")

        # Find the line number
        for i, line in enumerate(content.split('\n'), 1):
            if "self.global_state = global_state" in line:
                print(f"   → Found on line {i}: {line.strip()}")
                break
    else:
        print("   ✗ Missing: self.global_state = global_state")

    # Check __init__ method
    print("\n3. Checking SpatialOSLauncher.__init__ method:")
    in_init = False
    init_lines = []
    for line in content.split('\n'):
        if 'def __init__(self' in line and 'SpatialOSLauncher' in content[:content.index(line)].split('\n')[-20:]:
            in_init = True
        elif in_init:
            if line.strip().startswith('def ') and 'def __init__' not in line:
                break
            init_lines.append(line)

    if init_lines:
        print("   First 15 lines of __init__:")
        for line in init_lines[:15]:
            if line.strip():
                print(f"   {line}")

else:
    print(f"2. File NOT found: {spatial_os_path}")

print("\n4. Trying to import and inspect:")
try:
    # Add current directory to path
    sys.path.insert(0, os.getcwd())

    from spatial_os import SpatialOSLauncher

    # Check if class has global_state in __init__
    import inspect
    init_source = inspect.getsource(SpatialOSLauncher.__init__)
    print("   ✓ Successfully imported SpatialOSLauncher")

    if "self.global_state" in init_source:
        print("   ✓ __init__ source contains self.global_state")
    else:
        print("   ✗ __init__ source MISSING self.global_state")
        print("\n   __init__ source code:")
        print(init_source)

    # Try to instantiate (without pygame)
    print("\n5. Checking global_state module:")
    try:
        from core.global_state import global_state as gs
        print(f"   ✓ global_state imported: {gs}")
        print(f"   ✓ global_state.mode: {gs.mode}")
    except Exception as e:
        print(f"   ✗ Failed to import global_state: {e}")

except Exception as e:
    print(f"   ✗ Failed to import: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Diagnostic complete")
print("=" * 70)
