from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    name: Optional[str]
    region: Optional[str]
    country: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    tz_id: Optional[str]
    localtime_epoch: Optional[int]
    localtime: Optional[str]
