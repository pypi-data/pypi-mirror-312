from dataclasses import dataclass
from typing import Optional, List

from weathercls.weatherapicom.forecast_weather.ForecastForecastday import ForecastForecastday


@dataclass
class Forecast:
    forecastday: Optional[List[ForecastForecastday]]
