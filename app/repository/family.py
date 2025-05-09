from app.models.family import Family as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="families"

class FamilyRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

