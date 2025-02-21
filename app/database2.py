import asyncpg
from fastapi import Depends

DATABASE_URL = "postgresql://postgres:bardiapostgres@127.0.0.1:5432/postgres"

# Function to connect to the database
async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)

# Dependency to get a database connection
async def get_db():
    connection = await get_db_connection()
    try:
        yield connection  # This allows the connection to be used in your routes
    finally:
        await connection.close()  # Ensure the connection is closed after use