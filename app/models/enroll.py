from pydantic import BaseModel, constr, conint, Field
from typing import Optional,List
from enum import Enum
from datetime import datetime,time


class Enroll(BaseModel):
    id: int  
    student_id: int 
    class_id: int 
    day: conint(ge=0, le=6) 
    time: time 
    status: conint(ge=0, le=1)
    credit: int 
    credit_spent: int 
    date_at: datetime 




