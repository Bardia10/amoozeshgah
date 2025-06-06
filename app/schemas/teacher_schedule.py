from typing import Optional,List
from pydantic import BaseModel, Field
from datetime import datetime,time
from app.models.teacher_schedule import TeacherSchedule 


class DayTime(BaseModel):
    day: int
    time: time

class GetPublicTeacherSchedulesResponse(BaseModel):
    items: List[DayTime]


class ClassEnrollment(BaseModel):
    time: time
    day: int  
    lastname: str  
    title: str    

class GetTeacherSchedulesResponse(BaseModel):
    classes: List[ClassEnrollment]
    busy: List[TeacherSchedule]


class CreateTeacherSchedule(TeacherSchedule):
    teacher_id: Optional[int]= Field(default=None)

class UpdateTeacherSchedules(BaseModel):
    free: List[CreateTeacherSchedule]
    busy: List[CreateTeacherSchedule]

class UpdateTeacherSchedulesResponse(BaseModel):
    message: str