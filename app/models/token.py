from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    id: Optional[int]= Field(default=None)
    user_id: int
    token: str
    created_at: datetime
    expires_at: datetime

