from typing import Optional,List
from pydantic import BaseModel
from datetime import datetime,time
from app.models.pseudo_paypal import PseudoPaypal as Item 



class GetPseudoPaypalResponse(BaseModel):
    item: Item


class PaypalCreateInput(BaseModel):
    amount: int
    token: str

class UpdatePseudoPaypalResponse(BaseModel):
    id: int
    message: str

class PaypalCreateResponse(BaseModel):
    id: int
    message: str