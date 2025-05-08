from typing import Optional,List
from pydantic import BaseModel
from datetime import datetime,time
from app.models.session import Session 





class GetEnrollsSessionsResponse(BaseModel):
    sessions: List[Session]

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