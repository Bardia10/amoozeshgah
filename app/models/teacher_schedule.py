from pydantic import BaseModel, constr, conint, Field
from typing import Optional
from datetime import datetime,time


class TeacherSchedule(BaseModel):
    teacher_id: int
    day: conint(ge=0, le=6)
    time: time


