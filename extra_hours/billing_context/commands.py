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
