from app.models.family import Family as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="families"

class FamilyRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

    async def get_by_parent(self, item_id: int):
        query = f"SELECT * FROM {self.table_name} WHERE category_id = $1"
        return await self.connection.fetch(query, item_id)