# src/database/db_utils.py

import os
import sys
import asyncpg
from functools import wraps
from datetime import datetime, date
import pandas as pd 


# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

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

def with_connection(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        pool = await DBPool.get_pool()
        async with pool.acquire() as conn:
            return await func(conn, *args, **kwargs)
    return wrapper

@with_connection
async def execute_query(conn, query, *args):
    return await conn.fetch(query, *args)





@with_connection
async def execute_many(conn, query, args_list):
    try:
        # Convert date strings and Timestamp objects to date objects and handle None values
        converted_args_list = []
        for args in args_list:
            converted_args = list(args)
            if isinstance(converted_args[2], (str, pd.Timestamp, datetime, date)):
                if isinstance(converted_args[2], str):
                    converted_args[2] = pd.to_datetime(converted_args[2]).date()
                elif isinstance(converted_args[2], pd.Timestamp):
                    converted_args[2] = converted_args[2].date()
                elif isinstance(converted_args[2], datetime):
                    converted_args[2] = converted_args[2].date()
                # If it's already a date object, leave it as is
            elif pd.isna(converted_args[2]):
                converted_args[2] = None
            else:
                print(f"Unexpected date type: {type(converted_args[2])}")
                continue
            
            converted_args = [None if pd.isna(arg) else arg for arg in converted_args]
            converted_args_list.append(tuple(converted_args))

        await conn.executemany(query, converted_args_list)
    except Exception as e:
        print(f"Error in execute_many: {e}")
        print(f"Query: {query}")
        print(f"Args: {args_list}")
        raise







@with_connection
async def execute_transaction(conn, *queries_and_args):
    async with conn.transaction():
        results = []
        for query, args in queries_and_args:
            result = await conn.fetch(query, *args)
            results.append(result)
        return results

if __name__ == "__main__":
    print("DB utilities imported successfully.")
    print(f"DB_HOST: {DB_HOST}")
    print(f"DB_NAME: {DB_NAME}")
