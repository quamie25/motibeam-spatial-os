#!/bin/bash
# MotiBeam Spatial OS - Setup Script
# Creates virtual environment and installs dependencies

set -e

echo "╔═══════════════════════════════════════╗"
echo "║  MotiBeam Spatial OS - Setup         ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Check if venv exists
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    echo "→ Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate and install
echo "→ Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║  Setup Complete!                     ║"
echo "╚═══════════════════════════════════════╝"
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "To run the Aviation ATC HUD:"
echo "  python3 scenes/aviation_realm.py"
echo ""
