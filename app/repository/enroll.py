from app.models.enroll import Enroll as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="enrolls"

class EnrollRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

