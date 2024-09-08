# src/data_processors/data_cleaner.py

import os
import sys
import pandas as pd


# Add the project root to the Python path
from src.utils.utils import add_project_root_to_path
add_project_root_to_path()

# Now you can import from src
from src.database.db_utils import execute_query, execute_many
from src.utils.logging_config import setup_logging

logger = setup_logging("data_cleaner")



async def clean_minute_data():
    # Fetch minute data, clean it, and update the database
    query = "SELECT * FROM minute_data"
    data = await execute_query(query)
    df = pd.DataFrame(data)
    
    # Perform cleaning operations (e.g., remove outliers, handle missing values)
    # ...

    # Update the cleaned data in the database
    update_query = """
    UPDATE minute_data
    SET open = $1, high = $2, low = $3, close = $4, volume = $5
    WHERE ticker_id = $6 AND timestamp = $7
    """
    await execute_many(update_query, df.to_records(index=False))

# Add similar functions for other data types (historical, financial)

async def main():
    await clean_minute_data()
    # Add calls to other cleaning functions

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
