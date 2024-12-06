from dataclasses import dataclass
from typing import List, Optional

from weathercls.weatherapicom.forecast_weather.ForecastAstro import ForecastAstro
from weathercls.weatherapicom.forecast_weather.ForecastDay import ForecastDay
from weathercls.weatherapicom.forecast_weather.ForecastHour import ForecastHour


@dataclass
class ForecastForecastday:
    date: Optional[str]
    date_epoch: Optional[int]
    day: Optional[ForecastDay]
    astro: Optional[ForecastAstro]
    hour: Optional[List[ForecastHour]]
