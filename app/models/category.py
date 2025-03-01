from pydantic import BaseModel, constr, conint, Field
from typing import Optional,List
from enum import Enum
from datetime import datetime


class Category(BaseModel):
    id: int  
    title: str 
    description: Optional[str] 
    image: Optional[str]


