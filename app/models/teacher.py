from pydantic import BaseModel, constr, conint
from typing import Optional,List




class Schedule(BaseModel): 
    time: str
    day: str    

class UpdateSchedules(BaseModel):
    teacher_id:int
    busy: List[Schedule]
    free: List[Schedule]

class UpdateSchedulesResponse(BaseModel):
    message: str

class ClassEnrollment(BaseModel):
    time: str
    day: str  
    lastname: str  
    title: str  
   

class GetSchedulesResponse(BaseModel):
    classes: List[ClassEnrollment]
    busy: List[Schedule]