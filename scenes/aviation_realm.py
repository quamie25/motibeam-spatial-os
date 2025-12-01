"""
Aviation Realm - ATC Sector Wall HUD
Neon-style Air Traffic Control display with radar, flight tracking, and weather alerts.
"""

import time
import random
import math
from datetime import datetime, timedelta
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich import box
import sys
import termios
import tty
import select


class ATCSectorHUD:
    """Air Traffic Control Sector Wall HUD with neon styling."""

    # Neon color scheme
    NEON_CYAN = "cyan"
    NEON_GREEN = "bright_green"
    NEON_YELLOW = "bright_yellow"
    NEON_MAGENTA = "bright_magenta"
    NEON_RED = "bright_red"
    NEON_BLUE = "bright_blue"

    def __init__(self):
        self.console = Console()
        self.current_view = 0
        self.views = ["sector_overview", "approach_focus", "weather_reroute"]
        self.running = True
        self.last_view_change = time.time()

        # Flight data
        self.flights = [
            {"callsign": "AA204", "alt": "FL320", "speed": "460 kts", "distance": "8 nm", "heading": 45, "status": "CRUISE"},
            {"callsign": "DL119", "alt": "FL280", "speed": "420 kts", "distance": "12 nm", "heading": 180, "status": "DESCEND"},
            {"callsign": "UA552", "alt": "FL350", "speed": "485 kts", "distance": "15 nm", "heading": 270, "status": "CRUISE"},
            {"callsign": "SW891", "alt": "FL260", "speed": "390 kts", "distance": "6 nm", "heading": 90, "status": "APPROACH"},
            {"callsign": "BA178", "alt": "FL300", "speed": "445 kts", "distance": "10 nm", "heading": 225, "status": "CRUISE"},
            {"callsign": "AF337", "alt": "FL240", "speed": "375 kts", "distance": "4 nm", "heading": 135, "status": "APPROACH"},
        ]

        self.focus_flight = self.flights[3]  # SW891 on approach

        # Arrivals/Departures
        self.arrivals = [
            {"callsign": "SW891", "origin": "ORD", "eta": "08:42", "status": "ON APPR"},
            {"callsign": "AF337", "origin": "CDG", "eta": "08:48", "status": "FINAL"},
            {"callsign": "BA178", "origin": "LHR", "eta": "09:05", "status": "HOLDING"},
            {"callsign": "AA204", "origin": "DFW", "eta": "09:12", "status": "CRUISE"},
        ]

        self.departures = [
            {"callsign": "DL551", "dest": "ATL", "etd": "08:45", "status": "CLEARED"},
            {"callsign": "UA223", "dest": "SFO", "etd": "08:50", "status": "TAXI"},
            {"callsign": "JB404", "dest": "BOS", "etd": "09:00", "status": "WAITING"},
        ]

        # Weather & alerts
        self.alerts = [
            "WINDS: 270° @ 18 kts GUSTING 25",
            "RUNWAY: 27L IN USE",
            "STORM CELL: 15 nm NORTH MOVING EAST",
            "REROUTE: AA204 → AVOID CHARLIE SECTOR",
            "VISIBILITY: 8 SM",
        ]

        self.ticker_offset = 0

    def _draw_radar_rings(self, size=20):
        """Draw concentric radar rings with flight positions."""
        lines = []
        center_x, center_y = size // 2, size // 2

        for y in range(size):
            line = ""
            for x in range(size):
                dx = x - center_x
                dy = y - center_y
                dist = math.sqrt(dx*dx + dy*dy)

                # Check if near a ring
                if abs(dist - 3) < 0.5 or abs(dist - 6) < 0.5 or abs(dist - 9) < 0.5:
                    line += "○"
                elif abs(dist) < 0.5:
                    line += "◎"
                else:
                    # Check for flight positions
                    flight_char = None
                    for i, flight in enumerate(self.flights[:6]):
                        # Position flights based on heading and distance
                        f_angle = math.radians(flight["heading"])
                        f_dist = int(flight["distance"].split()[0]) * 0.6
                        f_x = center_x + int(f_dist * math.cos(f_angle))
                        f_y = center_y - int(f_dist * math.sin(f_angle))

                        if x == f_x and y == f_y:
                            flight_char = "✈" if flight != self.focus_flight else "⬤"
                            break

                    line += flight_char if flight_char else " "

            lines.append(line)

        return "\n".join(lines)

    def _create_header(self):
        """Create the header panel."""
        header_text = Text()
        header_text.append("[A] AVIATION CONTROL", style=f"bold {self.NEON_CYAN}")
        header_text.append("\n")
        header_text.append("Airspace · Flight Paths · Collision Avoidance", style=self.NEON_GREEN)
        header_text.append("  ", style="")
        header_text.append("● ACTIVE SECTOR", style=f"bold {self.NEON_RED}")

        return Panel(
            Align.center(header_text),
            border_style=self.NEON_CYAN,
            box=box.DOUBLE,
        )

    def _create_radar_panel(self):
        """Create the radar sector panel."""
        content = Text()

        # Radar rings
        content.append("═══ SECTOR RADAR ═══\n\n", style=f"bold {self.NEON_CYAN}")
        radar = self._draw_radar_rings(18)
        content.append(radar, style=self.NEON_GREEN)

        # Flight list
        content.append("\n\n╔═══ TRACKED FLIGHTS ═══╗\n", style=f"bold {self.NEON_YELLOW}")

        for flight in self.flights[:6]:
            is_focus = flight == self.focus_flight
            style = self.NEON_MAGENTA if is_focus else self.NEON_CYAN
            prefix = "▶" if is_focus else "•"

            content.append(f"{prefix} {flight['callsign']}: ", style=f"bold {style}")
            content.append(f"{flight['alt']} · {flight['speed']} · {flight['distance']}\n", style=style)

        return Panel(
            content,
            border_style=self.NEON_CYAN,
            box=box.ROUNDED,
            title="[RADAR SECTOR]",
            title_align="left",
        )

    def _create_arrivals_departures_panel(self):
        """Create the arrivals/departures panel."""
        content = Text()

        # Arrivals
        content.append("╔═════ ARRIVALS ═════╗\n", style=f"bold {self.NEON_GREEN}")
        for arr in self.arrivals:
            status_color = self.NEON_RED if "FINAL" in arr["status"] else self.NEON_YELLOW
            content.append(f"▸ {arr['callsign']}", style=f"bold {self.NEON_CYAN}")
            content.append(f"\n  {arr['origin']} → ETA {arr['eta']}\n", style=self.NEON_CYAN)
            content.append(f"  {arr['status']}\n\n", style=status_color)

        # Departures
        content.append("\n╔═══ DEPARTURES ═══╗\n", style=f"bold {self.NEON_MAGENTA}")
        for dep in self.departures:
            status_color = self.NEON_GREEN if "CLEARED" in dep["status"] else self.NEON_YELLOW
            content.append(f"▸ {dep['callsign']}", style=f"bold {self.NEON_CYAN}")
            content.append(f"\n  → {dep['dest']} ETD {dep['etd']}\n", style=self.NEON_CYAN)
            content.append(f"  {dep['status']}\n\n", style=status_color)

        return Panel(
            content,
            border_style=self.NEON_MAGENTA,
            box=box.ROUNDED,
            title="[TRAFFIC]",
            title_align="left",
        )

    def _create_ticker(self):
        """Create scrolling alert ticker."""
        ticker_text = " ⬤ ".join(self.alerts)

        # Scroll effect
        display_text = ticker_text[self.ticker_offset:] + " ⬤⬤⬤ " + ticker_text[:self.ticker_offset]
        display_text = display_text[:100]  # Limit width

        self.ticker_offset = (self.ticker_offset + 2) % len(ticker_text)

        text = Text(display_text, style=f"bold {self.NEON_YELLOW}")

        return Panel(
            text,
            border_style=self.NEON_RED,
            box=box.HEAVY,
            title="[⚠ ALERTS]",
            title_align="left",
        )

    def _create_approach_focus_panel(self):
        """Create detailed approach focus view."""
        flight = self.focus_flight

        content = Text()
        content.append("╔═══════════════════════╗\n", style=f"bold {self.NEON_MAGENTA}")
        content.append("  APPROACH FOCUS MODE\n", style=f"bold {self.NEON_MAGENTA}")
        content.append("╚═══════════════════════╝\n\n", style=f"bold {self.NEON_MAGENTA}")

        content.append(f"⬤ FLIGHT: {flight['callsign']}\n\n", style=f"bold {self.NEON_CYAN} on black")

        content.append("ALTITUDE:    ", style=self.NEON_GREEN)
        content.append(f"{flight['alt']}\n", style=f"bold {self.NEON_YELLOW}")

        content.append("SPEED:       ", style=self.NEON_GREEN)
        content.append(f"{flight['speed']}\n", style=f"bold {self.NEON_YELLOW}")

        content.append("DISTANCE:    ", style=self.NEON_GREEN)
        content.append(f"{flight['distance']}\n", style=f"bold {self.NEON_YELLOW}")

        content.append("HEADING:     ", style=self.NEON_GREEN)
        content.append(f"{flight['heading']}°\n", style=f"bold {self.NEON_YELLOW}")

        content.append("STATUS:      ", style=self.NEON_GREEN)
        content.append(f"{flight['status']}\n\n", style=f"bold {self.NEON_RED}")

        content.append("─" * 30 + "\n", style=self.NEON_CYAN)
        content.append("CLEARANCE:\n", style=f"bold {self.NEON_MAGENTA}")
        content.append("  ✓ CLEARED ILS 27L\n", style=self.NEON_GREEN)
        content.append("  ✓ REDUCE TO 250 KTS\n", style=self.NEON_GREEN)
        content.append("  ✓ DESCEND 3000 FT\n", style=self.NEON_GREEN)
        content.append("\n  ⬤ ON GLIDE PATH\n", style=f"bold {self.NEON_CYAN}")

        return Panel(
            Align.center(content),
            border_style=self.NEON_MAGENTA,
            box=box.DOUBLE,
            title="[◈ APPROACH FOCUS ◈]",
            title_align="center",
        )

    def _create_weather_reroute_panel(self):
        """Create weather and rerouting view."""
        content = Text()

        content.append("╔═══════════════════════╗\n", style=f"bold {self.NEON_RED}")
        content.append(" WEATHER & REROUTING\n", style=f"bold {self.NEON_RED}")
        content.append("╚═══════════════════════╝\n\n", style=f"bold {self.NEON_RED}")

        # Weather section
        content.append("⚡ ACTIVE WEATHER:\n\n", style=f"bold {self.NEON_YELLOW}")

        content.append("  ⬤ STORM CELL\n", style=f"bold {self.NEON_RED}")
        content.append("    Position: 15 nm NORTH\n", style=self.NEON_CYAN)
        content.append("    Movement: EAST @ 12 kts\n", style=self.NEON_CYAN)
        content.append("    Intensity: MODERATE\n\n", style=self.NEON_YELLOW)

        content.append("  ⬤ WIND SHEAR ALERT\n", style=f"bold {self.NEON_RED}")
        content.append("    Altitude: Below 5000 ft\n", style=self.NEON_CYAN)
        content.append("    Winds: 270° @ 25G35\n\n", style=self.NEON_CYAN)

        content.append("─" * 30 + "\n\n", style=self.NEON_CYAN)

        # Rerouting section
        content.append("↻ ACTIVE REROUTES:\n\n", style=f"bold {self.NEON_MAGENTA}")

        content.append("  ▸ AA204\n", style=f"bold {self.NEON_CYAN}")
        content.append("    AVOID CHARLIE SECTOR\n", style=self.NEON_YELLOW)
        content.append("    NEW ROUTE: BRAVO → DELTA\n\n", style=self.NEON_GREEN)

        content.append("  ▸ BA178\n", style=f"bold {self.NEON_CYAN}")
        content.append("    HOLDING PATTERN\n", style=self.NEON_YELLOW)
        content.append("    REASON: TRAFFIC SPACING\n\n", style=self.NEON_GREEN)

        content.append("  ▸ DL119\n", style=f"bold {self.NEON_CYAN}")
        content.append("    EXPEDITE DESCENT\n", style=self.NEON_YELLOW)
        content.append("    REASON: STORM AVOIDANCE\n", style=self.NEON_GREEN)

        return Panel(
            Align.center(content),
            border_style=self.NEON_RED,
            box=box.DOUBLE,
            title="[⚠ WEATHER & REROUTES ⚠]",
            title_align="center",
        )

    def _create_sector_overview(self):
        """Create sector overview layout (radar + arrivals/departures)."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="main", ratio=1),
            Layout(name="ticker", size=3),
        )

        # Split main into left (radar) and right (arrivals/departures)
        layout["main"].split_row(
            Layout(name="radar", ratio=60),
            Layout(name="traffic", ratio=40),
        )

        layout["header"].update(self._create_header())
        layout["radar"].update(self._create_radar_panel())
        layout["traffic"].update(self._create_arrivals_departures_panel())
        layout["ticker"].update(self._create_ticker())

        return layout

    def _create_approach_focus_layout(self):
        """Create approach focus layout."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="main", ratio=1),
            Layout(name="ticker", size=3),
        )

        layout["header"].update(self._create_header())
        layout["main"].update(self._create_approach_focus_panel())
        layout["ticker"].update(self._create_ticker())

        return layout

    def _create_weather_reroute_layout(self):
        """Create weather & rerouting layout."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="main", ratio=1),
            Layout(name="ticker", size=3),
        )

        layout["header"].update(self._create_header())
        layout["main"].update(self._create_weather_reroute_panel())
        layout["ticker"].update(self._create_ticker())

        return layout

    def _get_current_layout(self):
        """Get the current view's layout."""
        view_name = self.views[self.current_view]

        if view_name == "sector_overview":
            return self._create_sector_overview()
        elif view_name == "approach_focus":
            return self._create_approach_focus_layout()
        elif view_name == "weather_reroute":
            return self._create_weather_reroute_layout()

    def _check_keyboard(self):
        """Check for keyboard input (non-blocking)."""
        if select.select([sys.stdin], [], [], 0)[0]:
            try:
                # Save terminal settings
                old_settings = termios.tcgetattr(sys.stdin)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)

                    # ESC key
                    if ord(ch) == 27:
                        self.running = False
                        return

                    # SPACE key
                    if ch == ' ':
                        self.current_view = (self.current_view + 1) % len(self.views)
                        self.last_view_change = time.time()

                finally:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            except:
                pass

    def run(self, duration=30):
        """
        Run the ATC HUD for a specified duration.

        Args:
            duration: How long to run in seconds (default 30)

        Controls:
            SPACE: Next view
            ESC: Exit
        """
        start_time = time.time()

        self.console.clear()
        self.console.print("[bold cyan]╔═══════════════════════════════════════╗[/]")
        self.console.print("[bold cyan]║  ATC SECTOR WALL HUD - INITIALIZING  ║[/]")
        self.console.print("[bold cyan]╚═══════════════════════════════════════╝[/]")
        self.console.print("\n[bright_green]Controls:[/] [yellow]SPACE[/] = Next View  [yellow]ESC[/] = Exit\n")
        time.sleep(2)

        with Live(self._get_current_layout(), refresh_per_second=4, console=self.console) as live:
            while self.running and (time.time() - start_time < duration):
                # Auto-cycle views every 4 seconds
                if time.time() - self.last_view_change > 4:
                    self.current_view = (self.current_view + 1) % len(self.views)
                    self.last_view_change = time.time()

                # Check for keyboard input
                self._check_keyboard()

                # Update display
                live.update(self._get_current_layout())

                time.sleep(0.25)

        self.console.clear()
        self.console.print("\n[bold cyan]╔═══════════════════════════════════════╗[/]")
        self.console.print("[bold cyan]║    ATC SECTOR WALL HUD - OFFLINE     ║[/]")
        self.console.print("[bold cyan]╚═══════════════════════════════════════╝[/]")
        self.console.print("\n[bright_green]Session complete. All flights handed off.[/]\n")


# Main entrypoint
def main():
    """Run the Aviation ATC HUD."""
    hud = ATCSectorHUD()
    hud.run(duration=60)


if __name__ == "__main__":
    main()
