from typing import Optional,List
from pydantic import BaseModel
from enum import Enum


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


