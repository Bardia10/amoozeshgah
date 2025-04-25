from app.models.teacher_schedule import TeacherSchedule as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="teacher_schedules"

class TeacherScheduleRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

    async def get_by_teacher(self, item_id: int):
        query = f"SELECT * FROM {self.table_name} WHERE teacher_id = $1"
        return await self.connection.fetchrow(query, item_id)

