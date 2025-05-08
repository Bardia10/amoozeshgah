from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime,time


class TeacherSchedule(BaseModel):
    teacher_id: int
    day: int
    time: time


