from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class CreateBillingCommand:
    user_id: UUID
    title: str
    description: str
    value: float
    work_date: Optional[datetime]


@dataclass
class ConfirmReceiveBillingCommand:
    user_id: UUID
    billing_id: UUID


@dataclass
class CancelReceiveBillingCommand:
    user_id: UUID
    billing_id: UUID


@dataclass
class UpdateBillingCommand:
    user_id: UUID
    billing_id: UUID
    title: str
    description: str
    value: float
    work_date: Optional[datetime]
