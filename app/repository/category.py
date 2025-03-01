from app.models.category import Category
from app.repository.common import CommonRepository 
from fastapi import Depends



item_repo = CommonRepository()


class CategoryRepository:
    async def get_all(self, connection):
        return await item_repo.get_all(connection,"categories")

    async def get_by_id(self, connection, item_id: int):
        return await item_repo.get_by_id(connection,"categories", item_id)

    async def create(self, connection, item: Category):
        return await item_repo.create(connection,"categories", item)

    async def delete_by_id(self, connection, item_id: int):
        return await item_repo.delete_by_id(connection,"categories", item_id)
