from app.models.course import Course as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="courses"

class CourseRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

