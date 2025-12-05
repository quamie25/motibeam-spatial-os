#!/bin/bash
# MotiBeam Auto-Boot Setup Script
# Configures MotiBeam to launch automatically on Pi startup

echo "═══════════════════════════════════════════════════════"
echo "  MOTIBEAM AUTO-BOOT SETUP"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Choose auto-boot method:"
echo ""
echo "  1) Desktop Autostart (launches after login) - RECOMMENDED"
echo "  2) Systemd Service (launches at boot, before login)"
echo "  3) Remove auto-boot"
echo "  4) Exit without changes"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "Installing Desktop Autostart..."

        # Make launch script executable
        chmod +x ~/motibeam-spatial-os/launch_motibeam.sh

        # Create autostart directory if it doesn't exist
        mkdir -p ~/.config/autostart

        # Copy desktop file to autostart
        cp ~/motibeam-spatial-os/motibeam.desktop ~/.config/autostart/

        # Make desktop file executable
        chmod +x ~/.config/autostart/motibeam.desktop

        echo "✓ Desktop autostart configured!"
        echo ""
        echo "MotiBeam will now launch automatically when you log in."
        echo "To test, logout and log back in, or reboot your Pi."
        ;;

    2)
        echo ""
        echo "Installing Systemd Service..."
        echo "This requires sudo permissions."

        # Make launch script executable
        chmod +x ~/motibeam-spatial-os/launch_motibeam.sh

        # Copy service file to systemd
        sudo cp ~/motibeam-spatial-os/motibeam.service /etc/systemd/system/

        # Reload systemd
        sudo systemctl daemon-reload

        # Enable service
        sudo systemctl enable motibeam.service

        echo "✓ Systemd service installed!"
        echo ""
        echo "MotiBeam will now launch automatically at boot."
        echo "To start now: sudo systemctl start motibeam"
        echo "To check status: sudo systemctl status motibeam"
        ;;

    3)
        echo ""
        echo "Removing auto-boot..."

        # Remove desktop autostart
        rm -f ~/.config/autostart/motibeam.desktop

        # Remove systemd service
        sudo systemctl stop motibeam.service 2>/dev/null
        sudo systemctl disable motibeam.service 2>/dev/null
        sudo rm -f /etc/systemd/system/motibeam.service
        sudo systemctl daemon-reload

        echo "✓ Auto-boot removed!"
        ;;

    4)
        echo ""
        echo "No changes made. Exiting."
        exit 0
        ;;

    *)
        echo ""
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Setup complete!"
echo "═══════════════════════════════════════════════════════"
