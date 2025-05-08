from typing import Optional,List
from pydantic import BaseModel
from app.models.enroll import Enroll as Item
from datetime import datetime,time

class EnrollCreate(Item):
    id: Optional[int] = None 


class EnrollSubmit(BaseModel):
    firstname: str
    lastname: str
    bio: str
    phone: str
    ssn: str
    birth_year: int
    class_id: int
    day: int
    time: time


class GetEnrollResponse(BaseModel):
    item: Item


class GetEnrollsResponse(BaseModel):
    items: List[Item]

    
class PostEnrollResponse(BaseModel):
    id : int
    message: str

class SubmitEnrollResponse(BaseModel):
    url : str
    message: str

class DeleteEnrollResponse(BaseModel):
    id : int
    message: str


class VerifyEnrollResponse(BaseModel):
    message: str