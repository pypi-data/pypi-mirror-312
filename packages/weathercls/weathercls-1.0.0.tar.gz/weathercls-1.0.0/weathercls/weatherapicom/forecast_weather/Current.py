from dataclasses import dataclass
from typing import Optional, Union

from weathercls.weatherapicom.forecast_weather.CurrentAirQuality import CurrentAirQuality
from weathercls.weatherapicom.forecast_weather.CurrentCondition import CurrentCondition


@dataclass
class Current:
    last_updated_epoch: Optional[int]
    last_updated: Optional[str]
    temp_c: Optional[float]
    temp_f: Optional[float]
    is_day: Optional[int]
    condition: Optional[CurrentCondition]
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
    vis_km: Optional[float]
    vis_miles: Optional[float]
    uv: Optional[Union[int, float]]
    gust_mph: Optional[float]
    gust_kph: Optional[float]
    air_quality: Optional[CurrentAirQuality]
