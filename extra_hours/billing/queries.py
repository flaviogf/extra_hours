from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BillingListQueryResult:
    uid: str
    title: str
    value: Decimal
