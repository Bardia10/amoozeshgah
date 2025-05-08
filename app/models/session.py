from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime,time


class Session(BaseModel):
    id: Optional[int]= Field(default=None)
    enroll_id: int
    jalali_date: str
    date_at: datetime
    deleted_at: Optional[datetime] = None
    time: time
    day: int

