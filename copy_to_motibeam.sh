#!/bin/bash
# Copy updated MotiBeam files to motibeam user directory

SOURCE_DIR="/home/user/motibeam-spatial-os"
TARGET_DIR="/home/motibeam/motibeam-spatial-os"

echo "Copying updated MotiBeam files..."
echo "From: $SOURCE_DIR"
echo "To: $TARGET_DIR"

# Copy Python files
cp -v "$SOURCE_DIR/spatial_os_ambient.py" "$TARGET_DIR/"
cp -v "$SOURCE_DIR/requirements.txt" "$TARGET_DIR/"

# Copy core directory
cp -rv "$SOURCE_DIR/core" "$TARGET_DIR/"

# Copy realms directory
cp -rv "$SOURCE_DIR/realms" "$TARGET_DIR/"

# Clear any Python cache
rm -rf "$TARGET_DIR/core/__pycache__"
rm -rf "$TARGET_DIR/core/ui/__pycache__"
rm -rf "$TARGET_DIR/realms/__pycache__"

# Set ownership to motibeam user
chown -R motibeam:motibeam "$TARGET_DIR"

echo ""
echo "✅ Files copied successfully!"
echo ""
echo "Now run as motibeam user:"
echo "  cd ~/motibeam-spatial-os"
echo "  python3 spatial_os_ambient.py"
