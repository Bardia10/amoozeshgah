from pydantic import BaseModel, constr, conint, Field
from typing import Optional,List
from enum import Enum
from datetime import datetime


class Class(BaseModel):
    id: int  
    description: Optional[str] 
    price: int 
    course_id: int 
    teacher_id: int 
