#!/bin/bash
# MotiBeam Spatial OS Launch Script
# Easy launcher for Raspberry Pi

echo "═══════════════════════════════════════════════════════"
echo "  MOTIBEAM SPATIAL OS"
echo "  Launching ambient computing interface..."
echo "═══════════════════════════════════════════════════════"

# Navigate to MotiBeam directory
cd ~/motibeam-spatial-os || {
    echo "Error: Cannot find ~/motibeam-spatial-os directory"
    exit 1
}

# Clear Python cache to ensure latest code runs
echo "Clearing Python cache..."
rm -rf core/__pycache__ core/ui/__pycache__ realms/__pycache__ 2>/dev/null

# Set display (required for projection)
export DISPLAY=:0

# Launch MotiBeam
echo "Starting MotiBeam..."
python3 spatial_os_ambient.py

# If MotiBeam exits, show exit message
echo ""
echo "MotiBeam exited."
