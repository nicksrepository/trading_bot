# ticker_manager.py
import os
import asyncpg
import yfinance as yf
import logging

# Configure logging
logging.basicConfig(
    filename='ticker_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Database connection details
DB_HOST = "localhost"
DB_NAME = "trading_bot_db"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Ensure you set this environment variable

async def get_all_tickers():
    """Fetch all tickers from the database."""
    try:
        pool = await asyncpg.create_pool(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            min_size=5,
            max_size=20
        )

        async with pool.acquire() as conn:
            tickers = await conn.fetch("SELECT symbol FROM tickers")
            return [record['symbol'] for record in tickers]

    except Exception as e:
        logging.error(f"Failed to fetch tickers: {e}")
        return []

    finally:
        await pool.close()

# Other functions remain unchanged, but they will now pull tickers from the database



def fetch_ticker_metadata(symbol):
    """Fetch metadata for a specific ticker using yfinance."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        sector = info.get('sector', 'N/A')
        industry = info.get('industry', 'N/A')
        
        if sector == 'N/A' or industry == 'N/A':
            logging.warning(f"Missing sector/industry for {symbol}. Manual review may be required.")

        return {
            'symbol': symbol,
            'name': info.get('shortName', 'N/A'),
            'sector': sector,
            'industry': industry
        }
    except Exception as e:
        logging.error(f"Failed to fetch data for {symbol}: {e}")
        return None


