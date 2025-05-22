from typing import Optional,List
from pydantic import BaseModel
from app.models.instrument import Instrument as Item

class InstrumentCreate(Item):
    id: Optional[int] = None 

class GetInstrumentResponse(BaseModel):
    item: Item

column_info = [
 {
 "title": "id",
 "datatype": "int",
 "description": "ID of the instrument"
 },
 {
 "title": "title",
 "datatype": "str",
 "description": "Title of the instrument"
 },
 {
 "title": "family_id",
 "datatype": "int",
 "description": "ID of the associated family"
 },
 {
 "title": "description",
 "datatype": "str",
 "description": "Description of the instrument"
 },
 {
 "title": "image",
 "datatype": "str",
 "description": "Image URL of the instrument"
 }
]

class GetInstrumentsResponse(BaseModel):
    items: List[Item]
    column_info: list = column_info

    
class PostInstrumentResponse(BaseModel):
    id : int
    message: str

class DeleteInstrumentResponse(BaseModel):
    id : int
    message: str