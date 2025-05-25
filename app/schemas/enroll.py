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



column_info = [
  {
    "title": "id",
    "datatype": "int",
    "description": "ID of the enrollment record"
  },
  {
    "title": "student_id",
    "datatype": "int",
    "description": "ID of the associated student"
  },
  {
    "title": "class_id",
    "datatype": "int",
    "description": "ID of the associated class"
  },
  {
    "title": "day",
    "datatype": "int",
    "description": "Day of the week (0 for Sunday, 6 for Saturday)"
  },
  {
    "title": "time",
    "datatype": "time",
    "description": "Time of the enrollment"
  },
  {
    "title": "status",
    "datatype": "int",
    "description": "Status of the enrollment (0 for inactive, 1 for active)"
  },
  {
    "title": "credit",
    "datatype": "int",
    "description": "Total credits assigned to the enrollment"
  },
  {
    "title": "credit_spent",
    "datatype": "int",
    "description": "Credits spent by the enrollment"
  },
  {
    "title": "date_at",
    "datatype": "datetime",
    "description": "Date and time when the enrollment was created"
  }
]

class GetEnrollsResponse(BaseModel):
    items: List[Item]
    column_info: list = column_info

    
class PostEnrollResponse(BaseModel):
    id : int
    message: str

class SubmitEnrollResponse(BaseModel):
    url : str
    message: str
    token: str
    url_expiration: datetime
    url_token: str

class DeleteEnrollResponse(BaseModel):
    id : int
    message: str


class VerifyEnrollResponse(BaseModel):
    message: str

class EnrollUpdate(Item):
    id: Optional[int] = None

class UpdateEnrollResponse(BaseModel):
    id: int
    message: str