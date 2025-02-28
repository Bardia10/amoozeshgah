from app.models.item import Item
from fastapi import Depends

class ItemRepository:
    async def get_all(self, connection):
        query = "SELECT * FROM items"
        return await connection.fetch(query)

    async def get_by_id(self, connection, item_id: int):
        query = "SELECT * FROM items WHERE id = $1"
        return await connection.fetchrow(query, item_id)

    async def create(self, connection, item: Item):
        query = "INSERT INTO items (name, description) VALUES ($1, $2) RETURNING id"
        item_id = await connection.fetchval(query, item.name, item.description)
        item.id = item_id
        # return {**item.dict(), "id": item_id}
        return item