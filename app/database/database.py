import asyncpg

DATABASE_URL = "postgresql://postgres:bardiapostgres@127.0.0.1:5432/postgres"

# Function to connect to the database
async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)

