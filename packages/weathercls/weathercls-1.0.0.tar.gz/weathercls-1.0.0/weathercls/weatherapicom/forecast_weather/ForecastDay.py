from dataclasses import dataclass
from typing import Optional, Union

from weathercls.weatherapicom.forecast_weather.ForecastDayCondition import ForecastDayCondition


@dataclass
class ForecastDay:
    maxtemp_c: Optional[float]
    maxtemp_f: Optional[float]
    mintemp_c: Optional[float]
    mintemp_f: Optional[float]
    avgtemp_c: Optional[float]
    avgtemp_f: Optional[float]
    maxwind_mph: Optional[float]
    maxwind_kph: Optional[float]
    totalprecip_mm: Optional[float]
    totalprecip_in: Optional[float]
    avgvis_km: Optional[float]
    avgvis_miles: Optional[float]
    avghumidity: Optional[float]
    daily_will_it_rain: Optional[int]
    daily_chance_of_rain: Optional[float]
    daily_will_it_snow: Optional[int]
    daily_chance_of_snow: Optional[float]
    condition: Optional[ForecastDayCondition]
    uv: Optional[Union[int, float]]
