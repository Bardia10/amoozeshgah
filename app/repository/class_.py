from app.models.class_ import Class as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="classes"

class ClassRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

