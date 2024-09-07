# src/utils/utils.py

import os
import sys
import asyncpg



def add_project_root_to_path():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

   # Call the function immediately
add_project_root_to_path()

   # Now you can import from src
from src.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD


class DBPool:
    _pool = None
    
    @classmethod
    async def get_pool(cls):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                min_size=5,
                max_size=20
            )
        return cls._pool

async def get_db_connection():
    return await DBPool.get_pool()
if __name__ == "__main__":
    print("DBPool and get_db_connection imported successfully.")
    print(f"DB_HOST: {DB_HOST}")
    print(f"DB_NAME: {DB_NAME}")
