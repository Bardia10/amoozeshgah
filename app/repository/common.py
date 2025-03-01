
class CommonRepository:
    async def get_all(self, connection, table_name: str):
        query = f"SELECT * FROM {table_name}"
        return await connection.fetch(query)

    async def get_by_id(self, connection, table_name: str, item_id: int):
        query = f"SELECT * FROM {table_name} WHERE id = $1"
        return await connection.fetchrow(query, item_id)
    
    async def get_by_column(self, connection, table_name: str, column_name: str, column_value):
        query = f"SELECT * FROM {table_name} WHERE {column_name} = $1"
        return await connection.fetchrow(query, column_value)

    # async def create(self, connection, item: Item):
    #     query = "INSERT INTO categories (name, description) VALUES ($1, $2) RETURNING id"
    #     item_id = await connection.fetchval(query, item.name, item.description)
    #     item.id = item_id
    #     # return {**item.dict(), "id": item_id}
    #     return item

    async def create(self, connection, table_name: str, item):
        # Convert the item to a dictionary, excluding the 'id' if it's auto-incremented
        item_data = item.dict(exclude={"id"})
        
        # Prepare the fields and values for the SQL query
        columns = ', '.join(item_data.keys())
        placeholders = ', '.join(f'${i + 1}' for i in range(len(item_data)))
        values = list(item_data.values())

        # Create the SQL insert query
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING id"

        # Execute the query and retrieve the new item id
        item_id = await connection.fetchval(query, *values)
        item.id = item_id
        
        return item

    async def delete_by_id(self, connection, table_name: str, item_id: int):
        # Create the SQL delete query using the variable table name
        query = f"DELETE FROM {table_name} WHERE id = $1"

        # Execute the query
        result = await connection.execute(query, item_id)

        # Optionally return a confirmation message or the result of the operation
        return result 