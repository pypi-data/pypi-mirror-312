from dataclasses import dataclass
from typing import Optional, Union

from weathercls.weatherapicom.forecast_weather.ForecastCondition import ForecastCondition


@dataclass
class ForecastHour:
    time_epoch: Optional[int]
    time: Optional[str]
    temp_c: Optional[float]
    temp_f: Optional[float]
    is_day: Optional[int]
    condition: Optional[ForecastCondition]
    wind_mph: Optional[float]
    wind_kph: Optional[float]
    wind_degree: Optional[float]
    wind_dir: Optional[str]
    pressure_mb: Optional[float]
    pressure_in: Optional[float]
    precip_mm: Optional[float]
    precip_in: Optional[float]
    humidity: Optional[float]
    cloud: Optional[float]
    feelslike_c: Optional[float]
    feelslike_f: Optional[float]
    windchill_c: Optional[float]
    windchill_f: Optional[float]
    heatindex_c: Optional[float]
    heatindex_f: Optional[float]
    dewpoint_c: Optional[float]
    dewpoint_f: Optional[float]
    will_it_rain: Optional[int]
    chance_of_rain: Optional[float]
    will_it_snow: Optional[int]
    chance_of_snow: Optional[float]
    vis_km: Optional[float]
    vis_miles: Optional[float]
    gust_mph: Optional[float]
    gust_kph: Optional[float]
    uv: Optional[Union[int, float]]
