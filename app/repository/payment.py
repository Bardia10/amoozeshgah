from app.models.payment import Payment as Item
from app.repository.common import CommonRepository 
from fastapi import Depends
from datetime import datetime

table_name="payments"

class PaymentRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

    async def get_by_enroll(self, enroll_id: int):
        query = f"SELECT * FROM payments WHERE enroll_id = $1"
        return await self.connection.fetchrow(query, enroll_id)

    async def soft_delete(self, id: int):
        query = f"UPDATE payments SET  deleted_at = $1 WHERE id = $2"
        return await self.connection.fetchrow(query, datetime.utcnow(), id)
    
