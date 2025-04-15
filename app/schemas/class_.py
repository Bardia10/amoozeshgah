from typing import Optional,List
from pydantic import BaseModel
from app.models.class_ import Class as Item

class ClassCreate(Item):
    id: Optional[int] = None 

class GetClassResponse(BaseModel):
    item: Item


class GetClassesResponse(BaseModel):
    items: List[Item]

    
class PostClassResponse(BaseModel):
    id : int
    message: str

class DeleteClassResponse(BaseModel):
    id : int
    message: str