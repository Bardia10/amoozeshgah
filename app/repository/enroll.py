from app.models.enroll import Enroll as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="enrolls"

class EnrollRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

      
    async def get_by_teacher(self, teacher_id: int):
        query = f"SELECT enrolls.day,enrolls.time, users.lastname,courses.title FROM enrolls INNER JOIN classes ON enrolls.class_id = classes.id INNER JOIN users ON enrolls.student_id = users.id INNER JOIN courses ON classes.course_id = courses.id WHERE classes.teacher_id = $1 AND enrolls.status=1;"
        return await self.connection.fetch(query, teacher_id)

    async def get_public_by_teacher(self, teacher_id: int):
        query = f"SELECT enrolls.time, enrolls.day FROM enrolls INNER JOIN classes ON enrolls.class_id = classes.id WHERE classes.teacher_id = $1"
        return await self.connection.fetch(query, teacher_id)

    
    async def add_spent(self, id: int):
        # Fetch the current credit_spent value for the given id
        query = f"SELECT credit_spent FROM {self.table_name} WHERE id = $1"
        result = await self.connection.fetchrow(query, id)

        if not result:
            raise ValueError(f"No entry found for id {id}")

        current_spent = result['credit_spent']  # Extract the value from the result

        # Increment the credit_spent value
        new_spent = int(current_spent) + 1

        # Update the credit_spent column in the database
        query = f"UPDATE {self.table_name} SET credit_spent = $1 WHERE id = $2"
        await self.connection.execute(query, new_spent, id)

        return {"id": id, "credit_spent": new_spent}


    async def update_status(self, id: int, status:int):
        # Fetch the current credit_spent value for the given id
        query = f"UPDATE enrolls SET status = $1 WHERE id = $2"
        result = await self.connection.execute(query, status,id)


    async def get_for_student(self, student_id: int):
        query = """
        SELECT 
            enrolls.*, 
            teacher.firstname AS teacher_firstname,
            teacher.lastname AS teacher_lastname,
            courses.title AS course_title
        FROM 
            enrolls
        JOIN 
            classes ON enrolls.class_id = classes.id
        JOIN 
            users AS teacher ON classes.teacher_id = teacher.id
        JOIN 
            courses ON classes.course_id = courses.id
        WHERE 
            enrolls.student_id = $1 AND enrolls.status=1;
        """
        return await self.connection.fetch(query, student_id)