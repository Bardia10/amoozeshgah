from app.models.pay_token import PayToken as Item
from app.repository.common import CommonRepository 
from fastapi import Depends
from datetime import datetime

table_name="pay_tokens"

class PayTokenRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

    async def get_by_token(self, token: str):
        query = f"SELECT * FROM pay_tokens WHERE token = $1"
        return await self.connection.fetchrow(query, token)

    async def soft_delete(self, id: int):
        query = f"UPDATE pay_tokens SET  deleted_at = $1 WHERE id = $2"
        return await self.connection.fetchrow(query, datetime.utcnow(), id)
    
