from app.models.instrument import Instrument as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="instruments"

class InstrumentRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

    async def get_by_parent(self, item_id: int):
        query = f"SELECT * FROM {self.table_name} WHERE family_id = $1"
        return await self.connection.fetch(query, item_id)

