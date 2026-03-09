import asyncpg
import asyncio

DATABASE_URL = "postgresql://postgres:3141592@localhost/smolgo"

async def create_table():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users_information (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            registration TEXT NOT NULL,
            total_quests TEXT NOT NULL
        )
    ''')
    await conn.close()

asyncio.run(create_table())