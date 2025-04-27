from typing import Optional,List
from pydantic import BaseModel
from datetime import datetime,time
from app.models.teacher_schedule import TeacherSchedule 


class DayTime(BaseModel):
    day: str
    time: time

class GetPublicTeacherSchedulesResponse(BaseModel):
    items: List[DayTime]


class ClassEnrollment(BaseModel):
    time: str
    day: str  
    lastname: str  
    title: str    

class GetTeacherSchedulesResponse(BaseModel):
    classes: List[ClassEnrollment]
    busy: List[TeacherSchedule]
