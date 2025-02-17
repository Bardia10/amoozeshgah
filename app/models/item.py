from pydantic import BaseModel, constr, conint
from typing import Optional

class Item(BaseModel):
    id: conint(ge=0)
    name: constr(max_length=100)
    description: Optional[str] = None