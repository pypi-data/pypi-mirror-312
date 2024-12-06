from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AlertsAlert:
    headline: Optional[str]
    msgtype: Optional[str]
    severity: Optional[str]
    urgency: Optional[str]
    areas: Optional[str]
    category: Optional[str]
    certainty: Optional[str]
    event: Optional[str]
    note: Optional[str]
    effective: Optional[datetime]
    expires: Optional[datetime]
    desc: Optional[str]
    instruction: Optional[str]
