"""
MotiBeam Spatial OS - Weather Integration
Live weather data with fallback to simulated data
"""

import json
import random
from typing import Dict, Optional
from datetime import datetime


class WeatherProvider:
    """Weather data provider with API and simulation modes"""

    def __init__(self, api_key: Optional[str] = None, location: str = "Home"):
        self.api_key = api_key
        self.location = location
        self.last_update = None
        self.cached_data = None
        self.update_interval = 600  # Update every 10 minutes

        # Simulated weather conditions
        self.sim_conditions = [
            "Clear", "Partly Cloudy", "Cloudy", "Light Rain",
            "Sunny", "Overcast", "Fair"
        ]

    def get_weather(self) -> Dict[str, str]:
        """
        Get current weather data
        Returns dict with: temp, condition, location
        """
        current_time = datetime.now().timestamp()

        # Use cached data if recent
        if self.cached_data and self.last_update:
            if current_time - self.last_update < self.update_interval:
                return self.cached_data

        # Try API if key is provided
        if self.api_key:
            try:
                data = self._fetch_from_api()
                if data:
                    self.cached_data = data
                    self.last_update = current_time
                    return data
            except Exception as e:
                print(f"Weather API error: {e}")
                # Fall through to simulation

        # Use simulated data as fallback
        data = self._simulate_weather()
        self.cached_data = data
        self.last_update = current_time
        return data

    def _fetch_from_api(self) -> Optional[Dict[str, str]]:
        """
        Fetch weather from OpenWeatherMap API
        Requires: pip install requests
        """
        try:
            import requests

            # OpenWeatherMap API endpoint
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": self.location,
                "appid": self.api_key,
                "units": "imperial"  # Fahrenheit
            }

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()

            return {
                "temp": f"{int(data['main']['temp'])}°",
                "condition": data['weather'][0]['main'],
                "location": data['name']
            }

        except ImportError:
            print("Weather API requires 'requests' module: pip install requests")
            return None
        except Exception as e:
            print(f"Weather API fetch error: {e}")
            return None

    def _simulate_weather(self) -> Dict[str, str]:
        """Generate simulated weather data for demo"""
        # Realistic temperature range
        temp = random.randint(60, 85)

        # Pick condition
        condition = random.choice(self.sim_conditions)

        return {
            "temp": f"{temp}°",
            "condition": condition,
            "location": self.location
        }


# Global weather provider instance
_weather_provider = None


def get_weather_provider(api_key: Optional[str] = None,
                        location: str = "Home") -> WeatherProvider:
    """Get or create global weather provider"""
    global _weather_provider

    if _weather_provider is None:
        _weather_provider = WeatherProvider(api_key, location)

    return _weather_provider


def get_current_weather(api_key: Optional[str] = None,
                       location: str = "Home") -> Dict[str, str]:
    """Convenience function to get current weather"""
    provider = get_weather_provider(api_key, location)
    return provider.get_weather()
