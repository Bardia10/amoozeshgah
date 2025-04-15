from pydantic import BaseModel, constr, conint, Field
from typing import Optional,List
from enum import Enum
from datetime import datetime


class Course(BaseModel):
    id: int  
    title: str 
    description: Optional[str] 
    image: Optional[str]
    family_id: int 
    instrument_id: Optional[int] 

