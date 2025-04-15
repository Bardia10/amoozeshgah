from typing import Optional,List
from pydantic import BaseModel
from app.models.instrument import Instrument as Item

class InstrumentCreate(Item):
    id: Optional[int] = None 

class GetInstrumentResponse(BaseModel):
    item: Item


class GetInstrumentsResponse(BaseModel):
    items: List[Item]

    
class PostInstrumentResponse(BaseModel):
    id : int
    message: str

class DeleteInstrumentResponse(BaseModel):
    id : int
    message: str