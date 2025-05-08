import asyncpg
from config.settings import settings

DATABASE_URL = settings.database_url

# Function to connect to the database
async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)

