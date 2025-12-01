# MotiBeam Spatial OS

**Large-format command wall displays for operational contexts**

MotiBeam Spatial OS is a multi-realm ambient computing platform providing high-visibility, neon-themed displays optimized for readability from 8-10 feet. Perfect for operations centers, command walls, and large-format monitoring displays.

## 🎯 Features

- **Enterprise Workspace Realm** — "Operations War Room"
  - Performance KPIs (Sales, Tickets, Uptime, Meetings)
  - Team Focus panels (Engineering, Support, Sales)
  - Meeting control and upcoming events
  - Continuous operations ticker

- **Aviation Control Realm** — "ATC Sector Wall"
  - Radar sector display with concentric rings
  - Flight path tracking (5-6 flights with callsigns)
  - Arrival/Departure stack with ETAs and runway assignments
  - Weather and rerouting information

- **Maritime Operations Realm** — "Port Command Board"
  - Harbor view with zones (Inner Harbor, Outer Channel, Anchorage)
  - Vessel traffic tracking (4-5 ships with data)
  - Port operations (Tug ops, Berth activity, Customs, Security)
  - Sea state and weather routing

## 🎨 Design

- **Neon Theme**: Glowing cyan, magenta, and green on dark background
- **Large Fonts**: All text sized for 8-10 foot viewing distance
- **Auto-Cycling**: Each realm cycles through 3 modes every 4 seconds
- **Clean Layout**: Big panels, no clutter, high contrast

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd motibeam-spatial-os

# Install dependencies
pip install -r requirements.txt
```

### Running

```bash
python motibeam_spatial_os.py
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| **W** | Switch to Enterprise Workspace realm |
| **A** | Switch to Aviation Control realm |
| **M** | Switch to Maritime Operations realm |
| **SPACE** | Manually cycle to next mode within current realm |
| **ESC** | Exit application |

## 📋 Realm Modes

### Enterprise Workspace (W)
1. **Performance View** - Today's KPIs and team summary
2. **Team Health** - Detailed team status and focus
3. **Meeting Control** - Current and upcoming meetings

### Aviation Control (A)
1. **Sector Overview** - Full radar with all flights
2. **Approach Focus** - Detailed view of focus aircraft
3. **Weather Routing** - Weather conditions and rerouting

### Maritime Operations (M)
1. **Vessel Traffic** - Harbor zones with vessel positions
2. **Port Operations** - Tug ops, berths, customs, security
3. **Weather Routing** - Sea state and tide information

## 🏗️ Architecture

```
motibeam-spatial-os/
├── motibeam_spatial_os.py      # Main entry point
├── core/
│   ├── realm_base.py            # Abstract base class for realms
│   └── realm_manager.py         # Realm registration and switching
├── config/
│   └── theme_neon.py            # Neon theme configuration
└── scenes/
    ├── enterprise_workspace_realm.py
    ├── aviation_control_realm.py
    └── maritime_operations_realm.py
```

## 🛠️ Technical Details

- **Display Resolution**: 1920x1080 (Full HD)
- **Frame Rate**: 60 FPS
- **Auto-Cycle Interval**: 4 seconds per mode
- **Graphics Library**: Pygame 2.5.0+

## 📝 Adding New Realms

1. Create a new realm class inheriting from `RealmBase`
2. Implement required methods:
   - `get_modes()` - Return list of mode names
   - `render_mode(mode)` - Render the specified mode
   - `realm_name` and `realm_key` properties
3. Register the realm in `motibeam_spatial_os.py`

## 🎨 Customization

### Theme Colors
Edit `config/theme_neon.py` to customize colors:
- Primary: Cyan (0, 255, 255)
- Secondary: Magenta (255, 0, 255)
- Accent: Neon Green (0, 255, 128)
- Warning: Yellow (255, 255, 0)
- Danger: Red (255, 50, 50)

### Font Sizes
Adjust font sizes in `theme_neon.py` for different viewing distances.

## 📄 License

See LICENSE file for details.

## 🤝 Contributing

This is a foundation platform. Contributions for new realms (Clinical, Education, Transport, etc.) are welcome!
