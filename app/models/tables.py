from pydantic import BaseModel, constr, conint, Field
from typing import Optional,List
from enum import Enum
from datetime import datetime
class Role(str, Enum):
    admin = "admin"
    student = "student"
    teacher = "teacher"

class User(BaseModel):
    id: int
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

class Token(BaseModel):
    id: Optional[int]= Field(default=None)
    user_id: int
    token: str
    created_at: datetime
    expires_at: datetime

class Category(BaseModel):
    id: int  
    title: str 
    description: Optional[str] 
    image: Optional[str]