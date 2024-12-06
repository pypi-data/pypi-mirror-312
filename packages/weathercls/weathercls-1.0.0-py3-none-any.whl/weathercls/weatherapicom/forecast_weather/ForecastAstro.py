from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class ForecastAstro:
    sunrise: Optional[str]
    sunset: Optional[str]
    moonrise: Optional[str]
    moonset: Optional[str]
    moon_phase: Optional[str]
    moon_illumination: Optional[Union[str, int]]
