from typing import Optional,List
from pydantic import BaseModel
from app.models.family import Family as Item

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

    
class PostFamilyResponse(BaseModel):
    id : int
    message: str

class DeleteFamilyResponse(BaseModel):
    id : int
    message: str