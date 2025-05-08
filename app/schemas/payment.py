from typing import Optional,List
from pydantic import BaseModel
from datetime import datetime,time
from app.models.payment import Payment



class PaymentCreate(Payment):
        id: Optional[int] = None 



