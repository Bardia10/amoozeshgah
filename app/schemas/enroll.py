from typing import Optional,List
from pydantic import BaseModel
from app.models.enroll import Enroll as Item

class EnrollCreate(Item):
    id: Optional[int] = None 

class GetEnrollResponse(BaseModel):
    item: Item


class GetEnrollsResponse(BaseModel):
    items: List[Item]

    
class PostEnrollResponse(BaseModel):
    id : int
    message: str

class DeleteEnrollResponse(BaseModel):
    id : int
    message: str