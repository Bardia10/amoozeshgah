from typing import Optional,List
from pydantic import BaseModel
from app.models.course import Course as Item

class CourseCreate(Item):
    id: Optional[int] = None 

class GetCourseResponse(BaseModel):
    item: Item

column_info = [
 {
 "title": "id",
 "datatype": "int",
 "description": "ID of the course"
 },
 {
 "title": "title",
 "datatype": "str",
 "description": "Title of the course"
 },
 {
 "title": "description",
 "datatype": "str",
 "description": "Description of the course"
 },
 {
 "title": "image",
 "datatype": "str",
 "description": "Image URL of the course"
 },
 {
 "title": "family_id",
 "datatype": "int",
 "description": "ID of the associated family"
 },
 {
 "title": "instrument_id",
 "datatype": "int",
 "description": "ID of the associated instrument (optional)"
 }
]

class GetCoursesResponse(BaseModel):
    items: List[Item]
    column_info: list = column_info

    
class PostCourseResponse(BaseModel):
    id : int
    message: str

class DeleteCourseResponse(BaseModel):
    id : int
    message: str