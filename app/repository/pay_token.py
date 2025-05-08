from app.models.pay_token import PayToken as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="pay_tokens"

class PayTokenRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

        
    
