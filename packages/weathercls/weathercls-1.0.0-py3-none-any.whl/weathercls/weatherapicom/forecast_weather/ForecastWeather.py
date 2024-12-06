from dataclasses import dataclass
from typing import Optional

from weathercls.weatherapicom.forecast_weather.Alerts import Alerts
from weathercls.weatherapicom.forecast_weather.Current import Current
from weathercls.weatherapicom.forecast_weather.Forecast import Forecast
from weathercls.weatherapicom.forecast_weather.Location import Location


@dataclass
class ForecastWeather:
    location: Optional[Location]
    current: Optional[Current]
    forecast: Optional[Forecast]
    alerts: Optional[Alerts]
