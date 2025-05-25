from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PseudoPaypal(BaseModel):
    id: Optional[int]= None
    amount: int
    token: str
    is_done: bool
    expires_at: datetime

