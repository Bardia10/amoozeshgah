from typing import Optional,List
from pydantic import BaseModel
from app.models.course import Course as Item

class CourseCreate(Item):
    id: Optional[int] = None 

class GetCourseResponse(BaseModel):
    item: Item


class GetCoursesResponse(BaseModel):
    items: List[Item]

    
class PostCourseResponse(BaseModel):
    id : int
    message: str

class DeleteCourseResponse(BaseModel):
    id : int
    message: str