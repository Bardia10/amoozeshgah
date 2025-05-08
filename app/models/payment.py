from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Payment(BaseModel):
    id: Optional[int]= Field(default=None)
    enroll_id: int
    amount: int
    created_at: datetime
    deleted_at: Optional[datetime] = None

