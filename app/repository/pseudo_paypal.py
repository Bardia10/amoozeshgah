from app.models.pseudo_paypal import PseudoPaypal as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="pseudo_paypal"

class PseudoPaypalRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

    async def check_done(self, token: str, amount: int):
        query = f"SELECT * FROM {self.table_name} WHERE token = $1 AND amount = $2 AND is_done = $3"
        return await self.connection.fetchrow(query, token, amount, True)
