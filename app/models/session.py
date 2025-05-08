from pydantic import BaseModel, constr, conint, Field
from typing import Optional
from datetime import datetime,time


class Session(BaseModel):
    id: Optional[int]= Field(default=None)
    enroll_id: int
    jalali_date: constr(regex=r'^\d{4}/\d{2}/\d{2}$')
    date_at: datetime
    deleted_at: Optional[datetime] = None
    time: time
    day: conint(ge=0, le=6)

