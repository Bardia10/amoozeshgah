from pydantic import BaseModel, constr, conint, Field
from typing import Optional,List
from enum import Enum
from datetime import datetime,time


class Enroll(BaseModel):
    id: int  
    student_id: int 
    class_id: int 
    day: int 
    time: time 
    status: int 
    credit: int 
    credit_spent: int 
    date_at: datetime 




