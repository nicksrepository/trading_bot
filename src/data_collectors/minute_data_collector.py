import asyncio
import aiohttp
import logging
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.utils import add_project_root_to_path
add_project_root_to_path()

   # Now you can import other modules
from src.utils.logging_config import setup_logging
   # ... rest of your imports ...

### Add the parent directory of 'src' to the system path
##sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
##
from src.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD



print(f"sys.path: {sys.path}")
from src.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
print(f"DB_USER: {DB_USER}, DB_PASSWORD: {DB_PASSWORD}")



# Add the src directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.utils.logging_config import setup_logging
from src.utils.async_utils import async_retry, gather_with_concurrency
from src.database.db_utils import execute_many
from src.config import TICKERS, CONCURRENCY_LIMIT, DB_USER, DB_PASSWORD
print(f"DB_USER: {DB_USER}, DB_PASSWORD: {DB_PASSWORD[:2]}******")

logger = setup_logging("minute_data_collector")

@async_retry(max_retries=5)
async def fetch_minute_data(session, ticker):
    """
    Fetch minute data for a given ticker.

    Args:
        session (aiohttp.ClientSession): HTTP session for making requests.
        ticker (str): Stock symbol.

    Returns:
        dict or None: Minute data for the ticker, or None if the data is not found.
    """
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=1d'
        async with session.get(url) as response:
            if response.status == 404:
                logger.error(f"Minute data not found for {ticker} (404). Skipping...")
                return None
            response.raise_for_status()
            data = await response.json()
            logger.info(f"Fetched minute data for {ticker}")
            return data
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {e}")
        raise

async def process_minute_data(ticker, data):
    """
    Process and insert minute data into the database.

    Args:
        ticker (str): Stock symbol.
        data (dict): Minute data for the ticker.
    """
    try:
        chart_data = data['chart']['result'][0]
        timestamps = chart_data['timestamp']
        quote_data = chart_data['indicators']['quote'][0]

        records = [
            (ticker, ts, quote_data['open'][i], quote_data['high'][i], quote_data['low'][i], quote_data['close'][i], quote_data['volume'][i])
            for i, ts in enumerate(timestamps)
        ]

        query = """
        INSERT INTO minute_data (ticker_id, timestamp, open, high, low, close, volume)
        VALUES (
            (SELECT ticker_id FROM tickers WHERE symbol = $1),
            to_timestamp($2), $3, $4, $5, $6, $7
        )
        ON CONFLICT (ticker_id, timestamp) DO UPDATE
        SET open = EXCLUDED.open, high = EXCLUDED.high, low = EXCLUDED.low,
            close = EXCLUDED.close, volume = EXCLUDED.volume;
        """

        await execute_many(query, records)
        logger.info(f"Successfully inserted minute data for {ticker}")
    except Exception as e:
        logger.error(f"Error processing data for {ticker}: {e}")
        raise



async def main():
    """Main function to collect minute data for all tickers."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_minute_data(session, ticker) for ticker in TICKERS]
        results = await gather_with_concurrency(CONCURRENCY_LIMIT, *tasks)

        for ticker, data in zip(TICKERS, results):
            if data:
                await process_minute_data(ticker, data)

    logger.info("Minute data collection completed.")




if __name__ == "__main__":
    asyncio.run(main())
