#!/bin/bash

# MotiBeam Spatial OS - Launcher Script
# MOS-1.0 Kickstarter Demo

# Color codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                    MotiBeam Spatial OS Launcher                      ║"
echo "║                           MOS-1.0                                    ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    echo "Please install Python 3 to run MotiBeam Spatial OS."
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version 2>&1)
echo -e "${GREEN}✓${NC} Found: $PYTHON_VERSION"

# Change to script directory
cd "$(dirname "$0")"

# Check if main file exists
if [ ! -f "motibeam_spatial_os.py" ]; then
    echo -e "${RED}Error: motibeam_spatial_os.py not found!${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} MotiBeam Spatial OS files detected"
echo ""

# Parse command line arguments
MODE="interactive"
if [ "$1" == "--auto" ] || [ "$1" == "-a" ]; then
    MODE="auto"
    echo -e "${YELLOW}Starting in AUTO-LOOP DEMO mode...${NC}"
elif [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    python3 motibeam_spatial_os.py --help
    exit 0
else
    echo -e "${BLUE}Starting in INTERACTIVE MENU mode...${NC}"
    echo -e "${CYAN}(Use --auto for auto-loop demo mode)${NC}"
fi

echo ""
sleep 1

# Launch MotiBeam Spatial OS
if [ "$MODE" == "auto" ]; then
    python3 motibeam_spatial_os.py --auto
else
    python3 motibeam_spatial_os.py
fi

# Exit message
echo ""
echo -e "${CYAN}MotiBeam Spatial OS session ended.${NC}"
echo ""
