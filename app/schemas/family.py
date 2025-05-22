from typing import Optional,List
from pydantic import BaseModel
from app.models.family import Family as Item

column_info = [
 {
 "title": "id",
 "datatype": "int",
 "description": "ID of the family"
 },
 {
 "title": "title",
 "datatype": "str",
 "description": "Title of the family"
 },
 {
 "title": "description",
 "datatype": "str",
 "description": "Description of the family"
 },
 {
 "title": "image",
 "datatype": "str",
 "description": "Image URL of the family"
 },
 {
 "title": "category_id",
 "datatype": "int",
 "description": "ID of the associated category"
 }
]


class FamilyCreate(Item):
    id: Optional[int] = None 

class FamilyUpdate(Item):
    id: Optional[int] = None 

class UpdateFamilyResponse(BaseModel):
    id: int
    message: str

class GetFamilyResponse(BaseModel):
    item: Item


class GetFamiliesResponse(BaseModel):
    items: List[Item]
    column_info: list = column_info

    
class PostFamilyResponse(BaseModel):
    id : int
    message: str

class DeleteFamilyResponse(BaseModel):
    id : int
    message: str

