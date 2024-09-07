# src/data_processors/feature_engineering.py

import os
import sys
import pandas as pd

# Add the project root to the Python path
from src.utils.utils import add_project_root_to_path
add_project_root_to_path()

# Now you can import from src
from src.database.db_utils import execute_query, execute_many
from src.utils.logging_config import setup_logging

logger = setup_logging("feature_engineering")


async def calculate_technical_indicators():
    # Fetch historical data, calculate indicators, and store them
    query = "SELECT * FROM historical_data ORDER BY ticker_id, date"
    data = await execute_query(query)
    df = pd.DataFrame(data)
    
    # Calculate technical indicators
    df['sma_20'] = ta.trend.sma_indicator(df['close'], window=20)
    df['rsi'] = ta.momentum.rsi(df['close'])
    # Add more indicators as needed

    # Store the calculated indicators
    insert_query = """
    INSERT INTO technical_indicators (ticker_id, date, sma_20, rsi)
    VALUES ($1, $2, $3, $4)
    ON CONFLICT (ticker_id, date) DO UPDATE
    SET sma_20 = EXCLUDED.sma_20, rsi = EXCLUDED.rsi
    """
    await execute_many(insert_query, df[['ticker_id', 'date', 'sma_20', 'rsi']].to_records(index=False))

async def main():
    await calculate_technical_indicators()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
