from app.models.token import Token as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="tokens"

class TokenRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

        
    
