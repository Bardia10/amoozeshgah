from typing import Optional,List
from pydantic import BaseModel
from app.models.teacher_schedule import TeacherSchedule as Item


class GetTeacherScheduleResponse(BaseModel):
    item: Item

