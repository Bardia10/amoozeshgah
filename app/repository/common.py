
class CommonRepository:
    def __init__(self, connection, table_name: str, model):
        self.connection = connection
        self.table_name = table_name
        self.model = model  # The model to deal with the database

    async def get_all(self):
        query = f"SELECT * FROM {self.table_name}"
        return await self.connection.fetch(query)

    async def get_by_id(self, item_id: int):
        query = f"SELECT * FROM {self.table_name} WHERE id = $1"
        return await self.connection.fetchrow(query, item_id)

    async def get_by_column(self, column_name: str, column_value):
        query = f"SELECT * FROM {self.table_name} WHERE {column_name} = $1"
        return await self.connection.fetchrow(query, column_value)

    async def create(self, item):
        # Ensure the item is an instance of the provided model
        if not isinstance(item, self.model):
            raise ValueError(f"Expected an instance of {self.model.__name__}, got {type(item).__name__}")

        # Convert the item to a dictionary, excluding the 'id' if it's auto-incremented
        item_data = item.dict(exclude={"id"})

        # Prepare the fields and values for the SQL query
        columns = ', '.join(item_data.keys())
        placeholders = ', '.join(f'${i + 1}' for i in range(len(item_data)))
        values = list(item_data.values())

        # Create the SQL insert query
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders}) RETURNING id"

        # Execute the query and retrieve the new item id
        item_id = await self.connection.fetchval(query, *values)
        item.id = item_id
        
        return item

    async def delete_by_id(self, item_id: int):
        # Create the SQL delete query using the variable table name
        query = f"DELETE FROM {self.table_name} WHERE id = $1"

        # Execute the query
        result = await self.connection.execute(query, item_id)

        # Optionally return a confirmation message or the result of the operation
        return result

    async def update(self, item_id: int, item):
        # Ensure the item is an instance of the provided model
        if not isinstance(item, self.model):
            raise ValueError(f"Expected an instance of {self.model.__name__}, got {type(item).__name__}")

        # Convert the item to a dictionary, excluding 'id' as it's not updatable
        item_data = item.dict(exclude={"id"})

        # Prepare the fields and values for the SQL query
        set_clause = ', '.join(f"{key} = ${i + 1}" for i, key in enumerate(item_data.keys()))
        values = list(item_data.values())

        # Append the item_id to the values list for the WHERE clause
        values.append(item_id)

        # Create the SQL update query
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = ${len(values)}"

        # Execute the query
        result = await self.connection.execute(query, *values)

        # Return the result of the operation (e.g., number of rows updated)
        return result










# class CommonRepository:
#     async def get_all(self, connection, table_name: str):
#         query = f"SELECT * FROM {table_name}"
#         return await connection.fetch(query)

#     async def get_by_id(self, connection, table_name: str, item_id: int):
#         query = f"SELECT * FROM {table_name} WHERE id = $1"
#         return await connection.fetchrow(query, item_id)
    
#     async def get_by_column(self, connection, table_name: str, column_name: str, column_value):
#         query = f"SELECT * FROM {table_name} WHERE {column_name} = $1"
#         return await connection.fetchrow(query, column_value)

#     # async def create(self, connection, item: Item):
#     #     query = "INSERT INTO categories (name, description) VALUES ($1, $2) RETURNING id"
#     #     item_id = await connection.fetchval(query, item.name, item.description)
#     #     item.id = item_id
#     #     # return {**item.dict(), "id": item_id}
#     #     return item

#     async def create(self, connection, table_name: str, item):
#         # Convert the item to a dictionary, excluding the 'id' if it's auto-incremented
#         item_data = item.dict(exclude={"id"})
        
#         # Prepare the fields and values for the SQL query
#         columns = ', '.join(item_data.keys())
#         placeholders = ', '.join(f'${i + 1}' for i in range(len(item_data)))
#         values = list(item_data.values())

#         # Create the SQL insert query
#         query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING id"

#         # Execute the query and retrieve the new item id
#         item_id = await connection.fetchval(query, *values)
#         item.id = item_id
        
#         return item

#     async def delete_by_id(self, connection, table_name: str, item_id: int):
#         # Create the SQL delete query using the variable table name
#         query = f"DELETE FROM {table_name} WHERE id = $1"

#         # Execute the query
#         result = await connection.execute(query, item_id)

#         # Optionally return a confirmation message or the result of the operation
#         return result 