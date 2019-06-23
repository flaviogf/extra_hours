from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class AddBillingCommand:
    user_uid: str
    title: str
    description: str
    value: Decimal
    work_date: datetime