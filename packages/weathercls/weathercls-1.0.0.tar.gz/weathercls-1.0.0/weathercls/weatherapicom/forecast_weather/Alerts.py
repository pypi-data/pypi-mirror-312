from dataclasses import dataclass
from typing import List, Optional

from weathercls.weatherapicom.forecast_weather.AlertsAlert import AlertsAlert


@dataclass
class Alerts:
    alert: Optional[List[AlertsAlert]]
