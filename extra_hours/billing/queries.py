from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class BillingListQueryResult:
    uid: str
    title: str
    description: str
    value: Decimal
    work_date: datetime
    receive_date: Optional[datetime]
    received: bool
