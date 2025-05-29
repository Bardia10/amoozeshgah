from typing import Optional,List
from pydantic import BaseModel
from app.models.user import User , Role

class UserCreate(BaseModel):
    username: str
    password_hash: Optional[str] = None
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


column_info = [
 {
 "title": "id",
 "datatype": "int",
 "description": "ID of the user"
 },
 {
 "title": "username",
 "datatype": "str",
 "description": "Username of the user"
 },
 {
 "title": "password_hash",
 "datatype": "str",
 "description": "Hashed password of the user"
 },
 {
 "title": "firstname",
 "datatype": "str",
 "description": "First name of the user (optional)"
 },
 {
 "title": "lastname",
 "datatype": "str",
 "description": "Last name of the user (optional)"
 },
 {
 "title": "role",
 "datatype": "Role",
 "description": "Role of the user"
 },
 {
 "title": "bio",
 "datatype": "str",
 "description": "Biography of the user (optional)"
 },
 {
 "title": "ssn",
 "datatype": "str",
 "description": "Social Security Number of the user (optional)"
 },
 {
 "title": "contact",
 "datatype": "str",
 "description": "Contact information of the user (optional)"
 },
 {
 "title": "image",
 "datatype": "str",
 "description": "Image URL of the user (optional)"
 },
 {
 "title": "year_born",
 "datatype": "int",
 "description": "Year of birth of the user (optional)"
 }
]

class GetUsersResponse(BaseModel):
    items: List[User]
    column_info: list = column_info

    
class PostUserResponse(BaseModel):
    id : int
    message: str

class DeleteUserResponse(BaseModel):
    id : int
    message: str

class UserUpdate(User):
    id: Optional[int] = None

class UpdateUserResponse(BaseModel):
    id: int
    message: str

class UpdateUsersPassword(BaseModel):
    new_password: str

class UpdateUsersPasswordResponse(BaseModel):
        message: str



class TeacherPublic(BaseModel):
    id: int
    firstname: str
    lastname: str
    image:Optional[str] = None
class GetTeachersPublicResponse(BaseModel):
    items: List[TeacherPublic]