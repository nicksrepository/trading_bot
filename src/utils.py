# utils.py

import logging
import asyncpg
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, LOG_FORMAT, LOG_LEVEL

def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT
    )

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
