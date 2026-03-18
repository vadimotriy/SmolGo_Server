import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

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
            registration TEXT NOT NULL
        )
    ''')
    await conn.close()

asyncio.run(create_table())