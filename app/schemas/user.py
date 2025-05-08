from typing import Optional,List
from pydantic import BaseModel
from app.models.user import User , Role

class UserCreate(BaseModel):
    username: str
    password_hash: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    role: Role
    bio: Optional[str] = None
    ssn: Optional[str] = None
    contact: Optional[str] = None
    image: Optional[str] = None
    year_born: Optional[int] = None


class GetUserResponse(BaseModel):
    item: User


class GetUsersResponse(BaseModel):
    items: List[User]

    
class PostUserResponse(BaseModel):
    id : int
    message: str

class DeleteUserResponse(BaseModel):
    id : int
    message: str