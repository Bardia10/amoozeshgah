from app.models.class_ import Class as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="classes"

class ClassRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

    async def get_by_course(self, item_id: int):
        query = f"SELECT * FROM {self.table_name} WHERE course_id = $1"
        return await self.connection.fetch(query, item_id)

    async def get_by_teacher(self, item_id: int):
        query = f"SELECT * FROM {self.table_name} WHERE teacher_id = $1"
        return await self.connection.fetch(query, item_id)

