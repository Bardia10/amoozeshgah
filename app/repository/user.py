from app.models.user import User as Item
from app.repository.common import CommonRepository 
from fastapi import Depends

table_name="users"

class UserRepository(CommonRepository):
    def __init__(self, connection):
        super().__init__(connection, table_name, Item)

