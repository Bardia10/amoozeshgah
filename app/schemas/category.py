from typing import Optional,List
from pydantic import BaseModel
from app.models.category import Category as Item


column_info = [
  {
    "title": "id",
    "datatype": "int",
    "description": "ID of the object"
  },
  {
    "title": "title",
    "datatype": "str",
    "description": "Title of the object"
  },
  {
    "title": "description",
    "datatype": "str",
    "description": "Description of the object"
  },
  {
    "title": "image",
    "datatype": "str",
    "description": "Image URL of the object"
  }
]


class CategoryCreate(Item):
    id: Optional[int] = None 

class GetCategoryResponse(BaseModel):
    item: Item


class GetCategoriesResponse(BaseModel):
    items: List[Item]
    column_info: list = column_info

    
class PostCategoryResponse(BaseModel):
    id : int
    message: str

class DeleteCategoryResponse(BaseModel):
    id : int
    message: str