# motibeam-spatial-os
MotiBeam Spatial OS – multi-realm ambient computing platform for home, clinical, education, transport, and more.

## 🚀 Quick Start

### Setup

Run the setup script to create a virtual environment and install dependencies:

```bash
./setup.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Realms

**Aviation ATC HUD:**
```bash
source venv/bin/activate
python3 scenes/aviation_realm.py
```

Controls:
- `SPACE` - Next view
- `ESC` - Exit

## 📦 Available Realms

### Aviation Realm - ATC Sector Wall HUD
Neon-style Air Traffic Control display featuring:
- Real-time radar with flight tracking
- Arrivals and departures monitoring
- Weather alerts and rerouting information
- Three cycling views: Sector Overview, Approach Focus, Weather & Rerouting

## 🛠️ Development

Requirements:
- Python 3.8+
- Terminal with Unicode support
- 256-color terminal recommended for best neon effects

## 📝 License

See LICENSE file for details.
