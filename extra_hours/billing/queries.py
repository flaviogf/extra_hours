from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BillingReceivedListQueryResult:
    uid: str
    title: str
    value: Decimal
