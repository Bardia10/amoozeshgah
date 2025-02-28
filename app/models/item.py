from typing import Optional,List
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    description: str = None

class GetItemResponse(BaseModel):
    item: Item


class GetItemsResponse(BaseModel):
    items: List[Item]

    
class PostItemResponse(BaseModel):
    id : int
    message: str
