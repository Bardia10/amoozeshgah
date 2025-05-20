from typing import Optional,List
from pydantic import BaseModel
from app.models.category import Category as Item


column_info = [
  {
    "title": "id",
    "datatype": "int"
  },
  {
    "title": "title",
    "datatype": "str"
  },
  {
    "title": "description",
    "datatype": "str"
  },
  {
    "title": "image",
    "datatype": "str"
  }
]


class CategoryCreate(Item):
    id: Optional[int] = None 

class GetCategoryResponse(BaseModel):
    item: Item


class GetCategoriesResponse(BaseModel):
    items: List[Item]

    
class PostCategoryResponse(BaseModel):
    id : int
    message: str

class DeleteCategoryResponse(BaseModel):
    id : int
    message: str