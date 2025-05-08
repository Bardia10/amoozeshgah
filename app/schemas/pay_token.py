from typing import Optional,List
from pydantic import BaseModel
from datetime import datetime,time
from app.models.pay_token import PayToken 







class PayTokenCreate(PayToken):
        id: Optional[int] = None 



