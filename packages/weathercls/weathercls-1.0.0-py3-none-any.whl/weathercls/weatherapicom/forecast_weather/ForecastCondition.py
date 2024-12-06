from dataclasses import dataclass
from typing import Optional


@dataclass
class ForecastCondition:
    text: Optional[str]
    icon: Optional[str]
    code: Optional[int]
