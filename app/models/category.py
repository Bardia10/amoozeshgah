from typing import Optional,List
from pydantic import BaseModel

class Category(BaseModel):
    id: int
    title: str
    description: str = None
    image: str = None

class GetCategoryResponse(BaseModel):
    item: Category


class GetCategoriesResponse(BaseModel):
    items: List[Category]

    
class PostCategoryResponse(BaseModel):
    id : int
    message: str
