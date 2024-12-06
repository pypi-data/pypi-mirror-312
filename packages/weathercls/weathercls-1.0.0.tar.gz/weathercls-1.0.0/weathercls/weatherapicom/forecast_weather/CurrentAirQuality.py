from dataclasses import dataclass
from typing import Optional


@dataclass
class CurrentAirQuality:
    co: Optional[float]
    no2: Optional[float]
    o3: Optional[float]
    so2: Optional[float]
    pm2_5: Optional[float]
    pm10: Optional[float]
    us_epa_index: Optional[int]
    gb_defra_index: Optional[int]
