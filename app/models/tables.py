from pydantic import BaseModel, constr, conint, Field
from typing import Optional,List
from enum import Enum
from datetime import datetime


class Token(BaseModel):
    id: Optional[int]= Field(default=None)
    user_id: int
    token: str
    created_at: datetime
    expires_at: datetime

class Category(BaseModel):
    id: int  
    title: str 
    description: Optional[str] 
    image: Optional[str]