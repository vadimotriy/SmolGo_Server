import asyncpg

DATABASE_URL = "postgresql://postgres:3141592@localhost/smolgo"

async def get_db_connection():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()