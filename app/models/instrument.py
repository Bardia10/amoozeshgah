from typing import Optional,List
from pydantic import BaseModel
from enum import Enum



class Instrument(BaseModel):
    id: int
    title: str
    family_id: int
    description: Optional[str] = None
    image: Optional[str] = None



