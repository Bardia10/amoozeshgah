from fastapi import Depends
from app.database.db import get_db_connection

async def get_db():
    connection = await get_db_connection()
    try:
        yield connection
    finally:
        await connection.close()