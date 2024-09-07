import asyncpg

DB_HOST = "localhost"
DB_NAME = "trading_bot_db"
DB_USER = "postgres"
DB_PASSWORD = "dildobaggins"

async def test_db_connection():
    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connection successful")
        await conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

import asyncio
asyncio.run(test_db_connection())
