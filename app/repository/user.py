from app.schemas.user import UserCreate as Item
from app.repository.common import CommonRepository 
from fastapi import Depends



item_repo = CommonRepository()


class UserRepository:
    async def get_all(self, connection):
        return await item_repo.get_all(connection,"users")

    async def get_by_id(self, connection, item_id: int):
        return await item_repo.get_by_id(connection,"users", item_id)

    async def get_by_column(self, connection, column_name: str, column_value):
        return await item_repo.get_by_column(connection,"users", column_name, column_value)

    async def create(self, connection, item: Item):
        return await item_repo.create(connection,"users", item)

    async def delete_by_id(self, connection, item_id: int):
        return await item_repo.delete_by_id(connection,"users", item_id)

        
    
