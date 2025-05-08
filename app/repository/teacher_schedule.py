from app.models.teacher_schedule import TeacherSchedule as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="teacher_schedules"

class TeacherScheduleRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

    async def get_by_teacher(self, item_id: int):
        query = f"SELECT * FROM {self.table_name} WHERE teacher_id = $1"
        return await self.connection.fetch(query, item_id)

    async def get_public_by_teacher(self, item_id: int):
        query = f"SELECT day,time FROM {self.table_name} WHERE teacher_id = $1"
        return await self.connection.fetch(query, item_id)

    async def insert_many(self, items: list):
    # Ensure items is not empty
        if not items:
            return

        # Prepare the query for bulk insertion
        query = f"""
            INSERT INTO {self.table_name} (teacher_id, day, time)
            VALUES ($1, $2, $3)
        """

        # Prepare the data for insertion
        values = [(item.teacher_id, item.day, item.time) for item in items]

        # Use `executemany` for bulk insertion
        await self.connection.executemany(query, values)
        
    async def delete_many(self, items: list):
        # Ensure items is not empty
        if not items:
            return
        # Prepare the query for bulk deletion
        query = f"""
            DELETE FROM {self.table_name}
            WHERE teacher_id = $1 AND day = $2 AND time = $3
        """

        # Prepare the data for deletion
        values = [(item.teacher_id, item.day, item.time) for item in items]

        # Use `executemany` for bulk deletion
        await self.connection.executemany(query, values)

