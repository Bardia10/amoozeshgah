from typing import Optional,List
from pydantic import BaseModel
from app.models.class_ import Class as Item

class ClassCreate(Item):
    id: Optional[int] = None 

class GetClassResponse(BaseModel):
    item: Item

column_info = [
 {
 "title": "id",
 "datatype": "int",
 "description": "ID of the class"
 },
 {
 "title": "description",
 "datatype": "str",
 "description": "Description of the class"
 },
 {
 "title": "price",
 "datatype": "int",
 "description": "Price of the class"
 },
 {
 "title": "course_id",
 "datatype": "int",
 "description": "ID of the associated course"
 },
 {
 "title": "teacher_id",
 "datatype": "int",
 "description": "ID of the associated teacher"
 }
]

class GetClassesResponse(BaseModel):
    items: List[Item]
    column_info: list = column_info

    
class PostClassResponse(BaseModel):
    id : int
    message: str

class DeleteClassResponse(BaseModel):
    id : int
    message: str

class ClassUpdate(Item):
    id: Optional[int] = None

class UpdateClassResponse(BaseModel):
    id: int
    message: str