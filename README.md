# 🚀 MOTIBEAM SPATIAL OS

**Projection-based ambient computing platform for the living wall**

MotiBeam Spatial OS is a cinematic, projection-friendly interface system designed for 1920×1080 displays. Built for seniors, veterans, and OEM licensing, it transforms walls into living, breathing ambient computers.

---

## 🎯 KEY FEATURES

### ✨ Ambient Homescreen
- **9 Realm Orbs** — Navigate between different life domains (Clinical, TeleBeam, etc.)
- **Living Wall Background** — Particle system creates organic, flowing ambient motion
- **Soft Theme** — NO NEON. Projection-friendly colors readable from 10-15 feet
- **Live Date/Time** — Always-visible time display
- **Live Weather** — Real-time weather with OpenWeatherMap API (or simulated)
- **Scrolling Ticker** — Large, readable information feed
- **Privacy Mode** — Press `P` to blur/hide sensitive information
- **Fullscreen Mode** — Runs in true fullscreen for projection

### 🏥 Clinical & Health Realm (THE SHOWCASE)
- **4 Vitals Cards** — Heart rate, blood pressure, oxygen, temperature
- **Animated Sparklines** — Real-time trending graphs
- **True ECG Waveform** — Realistic P-QRS-T complex simulation
- **Body/Mind/Spirit** — Holistic wellness indicators
- **View Modes** — Dashboard (D), Body (B), Mind (M), Spirit (S)
- **Caregiver Alerts** — Press `C` to notify caregiver
- **Elder-Friendly** — Giant fonts, high contrast, visual-first

### 📞 TeleBeam (Ambient Telecommunications)
- **Visual Caller ID** — Room-wide caller cards
- **Trust Scoring** — Green (trusted), yellow (unknown), red (spam)
- **Ambient Alerts** — Breathing animations, not harsh rings
- **Call Actions** — Accept (A), Message (M), Decline (D)
- **Call History** — Track answered and missed calls
- **PTSD-Friendly** — No flashing or sudden movements
- **Privacy Mode** — Hide caller identity

---

## 📁 PROJECT STRUCTURE

```
motibeam-spatial-os/
├── spatial_os_ambient.py       # HOMESCREEN — Main entry point
├── core/
│   ├── ui/
│   │   └── framework.py        # UI components, animations, themes
│   └── weather.py              # Live weather integration
├── realms/
│   ├── base_realm.py           # Base class for all realms
│   ├── clinical_health.py      # Clinical & Health realm
│   └── telebeam.py             # TeleBeam telecommunications
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🛠️ INSTALLATION

### Prerequisites
- Python 3.8+
- Pygame 2.6+
- 1920×1080 display (for best experience)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Optional: Weather API Setup
To use real weather data (instead of simulated):

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Set environment variable:
   ```bash
   export OPENWEATHER_API_KEY="your-api-key-here"
   ```

---

## 🚀 USAGE

### Launch Homescreen
```bash
python3 spatial_os_ambient.py
```

### Homescreen Controls
| Key | Action |
|-----|--------|
| **Arrow Keys** | Navigate between realm orbs |
| **1-9** | Jump directly to realm |
| **Enter** | Launch selected realm |
| **P** | Toggle privacy mode |
| **C** | Notify caregiver |
| **I** | Simulate incoming call (TeleBeam demo) |
| **M** | Add missed call (TeleBeam demo) |
| **ESC** or **Q** | Quit |

### Clinical & Health Realm Controls
| Key | Action |
|-----|--------|
| **D** | Dashboard view (all vitals) |
| **B** | Body focus view |
| **M** | Mind focus view |
| **S** | Spirit focus view |
| **C** | Notify caregiver |
| **P** | Toggle privacy mode |
| **ESC** | Return to homescreen |

### TeleBeam Realm Controls
| Key | Action |
|-----|--------|
| **A** | Accept incoming call |
| **M** | Send message |
| **D** | Decline call |
| **H** | View call history |
| **I** | Simulate new incoming call |
| **P** | Toggle privacy mode |
| **ESC** | Return to homescreen |

---

## 🎨 DESIGN PHILOSOPHY

### This is NOT software. This is a living wall.

**Principles:**
- **Visual-first** — No paragraphs, no dense text
- **Large fonts only** — Readable from 10-15 feet away
- **Cinematic** — Breathing animations, soft glows, ambient feel
- **Elder-friendly** — High contrast, zero learning curve
- **PTSD-friendly** — No harsh flashing or sudden movements
- **Privacy-aware** — One-key toggle to hide sensitive data
- **Projection-optimized** — Soft colors, not harsh neon

**Think:**
- Apple TV aerial screensaver meets JARVIS interface
- Hospital ambient displays
- Smart home control without feeling like software

---

## 🏗️ CURRENT STATUS

### ✅ Completed
- [x] Core UI framework (themes, animations, particles)
- [x] Base realm architecture
- [x] Ambient homescreen with 9 orbs
- [x] Live date/time display
- [x] Live weather integration (with API support)
- [x] Scrolling info ticker
- [x] Privacy mode
- [x] Clinical & Health realm (fully implemented)
- [x] TeleBeam telecommunications realm
- [x] Fullscreen projection mode

### 🚧 Coming Soon (Not Yet Implemented)
- [ ] Daily Flow realm
- [ ] Learning realm
- [ ] Transport realm
- [ ] Wellness realm
- [ ] Entertainment realm
- [ ] Home Control realm
- [ ] Security realm
- [ ] Real IoT integrations
- [ ] Voice control
- [ ] Multi-user profiles

---

## 🎯 TARGET USE CASES

1. **OEM Licensing**
   - Hospitals & medical facilities
   - Senior living communities
   - Automotive in-cabin displays
   - Smart home manufacturers

2. **Kickstarter Demo**
   - Clinical & Health showcase
   - TeleBeam ambient calling
   - Living wall experience

3. **Consumer**
   - Disabled veterans
   - Elderly care
   - Smart home enthusiasts
   - Anyone wanting ambient computing

---

## 🧬 TECHNICAL DETAILS

### Performance Requirements
- **Target FPS:** 60
- **Platform:** Raspberry Pi 4+ or equivalent
- **Display:** 1920×1080 projector
- **Python:** 3.8+

### Architecture
- **Event-driven** — Each realm manages its own event loop
- **Display reuse** — No surface reloading (prevents flicker)
- **Cached rendering** — Fonts and assets cached for performance
- **Particle system** — 150 particles max for living background
- **Breathing animations** — Sine-wave based for smooth ambient motion

### Theme System
All colors are soft, muted, projection-friendly:
- **No harsh neon colors**
- **High contrast for readability**
- **Depth through glows and shadows**
- **Alpha blending for ambient effects**

---

## 🔐 PRIVACY MODE

Press `P` anywhere in the system to toggle privacy mode.

**What it does:**
- Hides personal names
- Replaces data with "••••"
- Obscures caller ID in TeleBeam
- Maintains UI structure (no layout shift)

**Use cases:**
- Demos and presentations
- Visitors in the home
- Screen recordings
- Public displays

---

## 📡 WEATHER INTEGRATION

### Using Real Weather API

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get free API key
3. Set environment variable:
   ```bash
   export OPENWEATHER_API_KEY="your-key"
   ```
4. Edit location in `spatial_os_ambient.py` (default: "Home")

### Simulated Weather (Default)

If no API key is provided, system uses realistic simulated weather:
- Random temperatures (60-85°F)
- Various conditions (Clear, Cloudy, Sunny, etc.)
- Updates every 60 seconds

---

## 🩺 CLINICAL REALM DETAILS

### Vitals Monitoring
- **Heart Rate** — Soft red, 60-100 BPM range
- **Blood Pressure** — Soft blue, 120/80 baseline
- **Oxygen Saturation** — Soft green, 95-100% range
- **Temperature** — Soft amber, 98.6°F baseline

### ECG Waveform
- **Realistic P-QRS-T complex** — Medically accurate shape
- **Animated in real-time** — Scrolling waveform
- **Breathing effect** — Subtle glow animation

### Body/Mind/Spirit Scores
- **Body** — Physical wellness (85%)
- **Mind** — Mental clarity (75%)
- **Spirit** — Emotional balance (90%)

### Subcategory Views
- **Body (B)** — Physical health details
- **Mind (M)** — Cognitive function
- **Spirit (S)** — Emotional wellness

---

## 📞 TELEBEAM DETAILS

### Trust Scoring System
- **1.0 (Green)** — Known contact, trusted
- **0.5-0.8 (Yellow)** — Unknown number
- **0.0-0.4 (Red)** — Likely spam

### Caller Card Features
- **Large name display** — Giant fonts
- **Phone number** — Secondary info
- **Reason/context** — Why they're calling
- **Trust bar** — Visual trust indicator
- **Action buttons** — Accept, Message, Decline

### Emergency Handling
- **VA Hotline** — Special priority
- **911 calls** — Overrides privacy mode
- **Caregiver calls** — High priority notifications

### PTSD-Friendly Design
- **No flashing** — Breathing animations only
- **Soft colors** — Not harsh or sudden
- **Gentle alerts** — Pulse effects, not rings
- **User control** — Always able to decline

---

## 🎭 OEM CUSTOMIZATION

MotiBeam is designed for white-label licensing:

### Customizable Elements
- Realm names and icons
- Color themes
- Ticker messages
- Default locations
- API integrations
- Logo and branding

### Integration Points
- **IoT devices** — Connect to real sensors
- **EMR systems** — Pull real health data
- **VoIP** — Real phone integration
- **Smart home** — Control lights, locks, etc.

---

## 🏁 DEVELOPMENT BRANCH

This build is on branch:
```
claude/resume-motibeam-development-01XLnF3PxgNhigYDTr7YPkVa
```

---

## 📜 LICENSE

See LICENSE file for details.

---

## 🙏 CREDITS

Built with Claude (Anthropic) for ambient computing innovation.

**Vision:** Make walls come alive. Make computing effortless. Make the future feel magical.

---

## 📬 CONTACT

For OEM licensing, partnerships, or inquiries, reach out via the repository.

---

**THIS IS NOT AN APP. THIS IS A LIVING WALL.**

Make it cinematic. Make it effortless. Make it magical. Make it impossible to ignore.

🚀 **MOTIBEAM** — The future of ambient computing.
