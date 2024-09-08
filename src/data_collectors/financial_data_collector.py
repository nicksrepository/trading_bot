# src/data_collectors/financial_data_collector.py

import asyncio
import yfinance as yf
from sqlalchemy.orm import Session
from src.database.db_utils import get_db
from src.models.ticker import Ticker
from src.config import TICKERS, CONCURRENCY_LIMIT
from src.utils.logging_config import setup_logging

logger = setup_logging("financial_data_collector")

async def fetch_financial_data(ticker: str):
    """
    Fetch financial data for a given ticker using yfinance.
    
    Args:
        ticker (str): Stock symbol.
        Returns:
        tuple: Ticker symbol and financial data.
    """
    try:
        stock = yf.Ticker(ticker)
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cash_flow
        return ticker, (financials, balance_sheet, cash_flow)
    except Exception as e:
        logger.error(f"Failed to fetch financial data for {ticker}: {e}")
        return ticker, None

async def process_financial_data(db: Session, ticker: str, data: tuple):
    """
    Process and insert financial data into the database.
    
    Args:
        db (Session): Database session.
        ticker (str): Stock symbol.
        data (tuple): Financial data tuple.
    """
    if data is None:
        logger.warning(f"No financial data available for {ticker}")
        return

    financials, balance_sheet, cash_flow = data
    
    # Process and insert data into the database
    # (Implement the logic to insert data into your financials table)

async def main():
    """
    Main function to collect financial data for all tickers.
    """
    db = next(get_db())
    tasks = [fetch_financial_data(ticker) for ticker in TICKERS]
    results = await asyncio.gather(*tasks)
    
    for ticker, data in results:
        await process_financial_data(db, ticker, data)

    logger.info("Financial data collection completed.")

if __name__ == "__main__":
    asyncio.run(main())