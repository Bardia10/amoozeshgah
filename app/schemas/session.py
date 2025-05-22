from typing import Optional,List
from pydantic import BaseModel
from datetime import datetime,time
from app.models.session import Session 


column_info = [
  {
    "title": "id",
    "datatype": "int",
    "description": "ID of the session record (optional)"
  },
  {
    "title": "enroll_id",
    "datatype": "int",
    "description": "ID of the associated enrollment"
  },
  {
    "title": "jalali_date",
    "datatype": "str",
    "description": "Jalali (Persian) date for the session"
  },
  {
    "title": "date_at",
    "datatype": "datetime",
    "description": "Date and time of the session"
  },
  {
    "title": "deleted_at",
    "datatype": "datetime",
    "description": "Date and time when the session was deleted (optional)"
  },
  {
    "title": "time",
    "datatype": "time",
    "description": "Time of the session"
  },
  {
    "title": "day",
    "datatype": "int",
    "description": "Day of the week for the session (0 for Sunday, 6 for Saturday)"
  }
]


class GetEnrollsSessionsResponse(BaseModel):
    sessions: List[Session]
    column_info: list = column_info

class SessionCreate(Session):
    class Config:
        fields = {"id": {"exclude": True}}


class SessionCreateInput(BaseModel):
    enroll_id: int
    time: time
    day: int
    week_delta: int



class SessionCreateResponse(BaseModel):
    message: str