from pydantic import BaseModel, constr, conint, Field
from typing import Optional,List
from enum import Enum
from datetime import datetime


class Enroll(BaseModel):
    id: int  
    student_id: int 
    class_id: int 
    day: str 
    time: str 
    status: int 
    credit: int 
    credit_spent: int 
    date_at: datetime 




