from app.models.enroll import Enroll as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="enrolls"

class EnrollRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

    async def get_by_teacher(self, teacher_id: int):
        query = f"SELECT enrolls.day,enrolls.time, users.lastname,courses.title FROM enrolls INNER JOIN classes ON enrolls.class_id = classes.id INNER JOIN users ON enrolls.student_id = users.id INNER JOIN courses ON classes.course_id = courses.id WHERE classes.teacher_id = $1;"
        return await self.connection.fetch(query, teacher_id)

    async def get_public_by_teacher(self, teacher_id: int):
        query = f"SELECT enrolls.time, enrolls.day FROM enrolls INNER JOIN classes ON enrolls.class_id = classes.id WHERE classes.teacher_id = $1"
        return await self.connection.fetch(query, teacher_id)

