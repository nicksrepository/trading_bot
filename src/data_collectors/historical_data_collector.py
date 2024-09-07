# src/data_collectors/historical_data_collector.py

import asyncio
import yfinance as yf
import sys
import os
##
##sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
##
##from src.utils.utils import add_project_root_to_path
##add_project_root_to_path()
##
##   # Now you can import other modules
##from src.utils.logging_config import setup_logging
##   # ... rest of your imports ...
##

# Add the src directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.utils.logging_config import setup_logging
from src.utils.async_utils import async_retry, gather_with_concurrency
from src.database.db_utils import execute_many
from src.config import TICKERS, CONCURRENCY_LIMIT

logger = setup_logging("historical_data_collector")

@async_retry(max_retries=3)
async def fetch_historical_data(ticker):
    """
    Fetch historical data for a given ticker.
    
    Args:
        ticker (str): Stock symbol.
    
    Returns:
        pandas.DataFrame: Historical data for the ticker.
    """
    try:
        data = yf.download(ticker, period="max", interval="1d")
        return ticker, data
    except Exception as e:
        logger.error(f"Failed to fetch data for {ticker}: {e}")
        raise

async def process_historical_data(ticker, data):
    """
    Process and insert historical data into the database.
    
    Args:
        ticker (str): Stock symbol.
        data (pandas.DataFrame): Historical data for the ticker.
    """
    if data.empty:
        logger.warning(f"No historical data available for {ticker}")
        return

    records = [
        (ticker, date, row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume'])
        for date, row in data.iterrows()
    ]

    query = """
    INSERT INTO historical_data (ticker_id, date, open, high, low, close, adjusted_close, volume)
    VALUES (
        (SELECT ticker_id FROM tickers WHERE symbol = $1),
        $2, $3, $4, $5, $6, $7, $8
    )
    ON CONFLICT (ticker_id, date) DO UPDATE
    SET open = EXCLUDED.open, high = EXCLUDED.high, low = EXCLUDED.low,
        close = EXCLUDED.close, adjusted_close = EXCLUDED.adjusted_close, volume = EXCLUDED.volume;
    """

    try:
        await execute_many(query, records)
        logger.info(f"Successfully inserted historical data for {ticker}")
    except Exception as e:
        logger.error(f"Failed to insert historical data for {ticker}: {e}")

async def main():
    """Main function to collect historical data for all tickers."""
    tasks = [fetch_historical_data(ticker) for ticker in TICKERS]
    results = await gather_with_concurrency(CONCURRENCY_LIMIT, *tasks)

    for ticker, data in results:
        if data is not None:
            await process_historical_data(ticker, data)

    logger.info("Historical data collection completed.")

if __name__ == "__main__":
    asyncio.run(main())
