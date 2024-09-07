# src/data_collectors/financial_data_collector.py

import yfinance as yf
import sys
import os
import asyncio
import pandas as pd
from datetime import datetime, date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.utils import add_project_root_to_path
add_project_root_to_path()

from src.utils.logging_config import setup_logging
from src.utils.async_utils import async_retry, gather_with_concurrency
from src.database.db_utils import execute_many
from src.config import TICKERS, CONCURRENCY_LIMIT, FINANCIAL_DATA_YEARS

logger = setup_logging("financial_data_collector")

def safe_get(df, row, col):
    try:
        return df.loc[row, col]
    except:
        return None

@async_retry(max_retries=3)
async def fetch_financial_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        income_statement = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cash_flow
        return ticker, (income_statement, balance_sheet, cash_flow)
    except Exception as e:
        logger.error(f"Failed to fetch financial data for {ticker}: {e}")
        return ticker, None




async def process_financial_data(ticker, data):
    if data is None:
        logger.warning(f"No financial data available for {ticker}")
        return

    income_statement, balance_sheet, cash_flow = data
    records = []

    for report_date in income_statement.columns:
        record = (
            ticker,
            'annual',
            report_date,  # Keep this as is, we'll handle conversion in execute_many
            safe_get(income_statement, 'Total Revenue', report_date),
            safe_get(income_statement, 'Net Income', report_date),
            safe_get(income_statement, 'Basic EPS', report_date)
        )
        records.append(record)

    query = """
    INSERT INTO financials (ticker_id, period, report_date, revenue, net_income, earnings_per_share)
    VALUES (
        (SELECT ticker_id FROM tickers WHERE symbol = $1),
        $2, $3, $4, $5, $6
    )
    ON CONFLICT (ticker_id, report_date) DO UPDATE
    SET revenue = EXCLUDED.revenue,
        net_income = EXCLUDED.net_income,
        earnings_per_share = EXCLUDED.earnings_per_share;
    """

    try:
        await execute_many(query, records)
        logger.info(f"Successfully inserted financial data for {ticker}")
    except Exception as e:
        logger.error(f"Failed to insert financial data for {ticker}: {e}")
        for record in records:
            logger.debug(f"Record for {ticker}: {record}")





async def main():
    """Main function to collect financial data for all tickers."""
    tasks = [fetch_financial_data(ticker) for ticker in TICKERS]
    results = await gather_with_concurrency(CONCURRENCY_LIMIT, *tasks)

    for ticker, data in results:
        if data is not None:
            await process_financial_data(ticker, data)

    logger.info("Financial data collection completed.")

if __name__ == "__main__":
    asyncio.run(main())
