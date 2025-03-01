from typing import Optional,List
from pydantic import BaseModel
from app.models.tables import User as Item

class UserCreate(Item):
    id: Optional[int] = None 

class GetUserResponse(BaseModel):
    item: Item


class GetUsersResponse(BaseModel):
    items: List[Item]

    
class PostUserResponse(BaseModel):
    id : int
    message: str

class DeleteUserResponse(BaseModel):
    id : int
    message: str