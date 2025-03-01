from app.models.family import Family
from app.repository.common import CommonRepository 
from fastapi import Depends



item_repo = CommonRepository()
table_name="families"


class CategoryRepository:
    async def get_all(self, connection):
        return await item_repo.get_all(connection,table_name)

    async def get_by_id(self, connection, item_id: int):
        return await item_repo.get_by_id(connection,table_name, item_id)

    async def create(self, connection, item: Family):
        return await item_repo.create(connection,table_name, item)

    async def delete_by_id(self, connection, item_id: int):
        return await item_repo.delete_by_id(connection,table_name, item_id)
