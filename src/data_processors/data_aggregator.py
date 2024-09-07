# src/data_processors/data_aggregator.py

import sys
import os
import pandas as pd
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.database.db_utils import execute_query, execute_many
from src.utils.logging_config import setup_logging

logger = setup_logging("data_aggregator")

async def aggregate_minute_to_hourly():
    # Fetch minute data, aggregate to hourly, and store the result
    query = "SELECT * FROM minute_data ORDER BY ticker_id, timestamp"
    data = await execute_query(query)
    
    if not data:
        logger.info("No minute data available for aggregation.")
        return
    
    df = pd.DataFrame(data, columns=['ticker_id', 'timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Set timestamp as index
    df.set_index('timestamp', inplace=True)
    
    # Aggregate to hourly data
    hourly_data = df.groupby(['ticker_id', pd.Grouper(freq='h')]).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).reset_index()

    # Store the aggregated data
    insert_query = """
    INSERT INTO hourly_data (ticker_id, timestamp, open, high, low, close, volume)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    ON CONFLICT (ticker_id, timestamp) DO UPDATE
    SET open = EXCLUDED.open, high = EXCLUDED.high, low = EXCLUDED.low,
        close = EXCLUDED.close, volume = EXCLUDED.volume
    """
    await execute_many(insert_query, hourly_data.values.tolist())
    logger.info(f"Aggregated and inserted {len(hourly_data)} hourly records")

async def main():
    await aggregate_minute_to_hourly()
    logger.info("Data aggregation completed.")

if __name__ == "__main__":
    asyncio.run(main())
    
