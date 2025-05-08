from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PayToken(BaseModel):
    id : int
    enroll_id: int
    token: str
    created_at: datetime
    deleted_at: Optional[datetime] = None
    expires_at: datetime

