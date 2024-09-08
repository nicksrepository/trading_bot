    # src/data_processors/feature_engineering.py

import pandas as pd
import ta
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.db_utils import get_db
from src.models.ticker import Ticker
from src.models.historical_data import HistoricalData
from src.models.technical_indicators import TechnicalIndicator
from src.utils.logging_config import setup_logging

logger = setup_logging("feature_engineering")

def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate technical indicators for a given DataFrame.
        
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data.
    
    Returns:
        pd.DataFrame: DataFrame with added technical indicators.
    """
    df['sma_20'] = ta.trend.sma_indicator(df['close'], window=20)
    df['rsi'] = ta.momentum.rsi(df['close'])
    df['macd'] = ta.trend.macd_diff(df['close'])
    df['bollinger_hband'] = ta.volatility.bollinger_hband(df['close'])
    df['bollinger_lband'] = ta.volatility.bollinger_lband(df['close'])
    return df

def process_historical_data(db: Session):
    """
    Process historical data and calculate technical indicators.
    
    Args:
        db (Session): Database session.
    """
    logger.info("Starting to process historical data")

    # Fetch all tickers
    tickers = db.query(Ticker).all()

    for ticker in tickers:
        logger.info(f"Processing data for ticker: {ticker.symbol}")

        # Fetch historical data for the current ticker
        stmt = select(HistoricalData).where(HistoricalData.ticker_id == ticker.ticker_id).order_by(HistoricalData.date)
        historical_data = db.execute(stmt).scalars().all()

        if not historical_data:
            logger.warning(f"No historical data found for ticker: {ticker.symbol}")
            continue

        # Convert to DataFrame
        df = pd.DataFrame([data.__dict__ for data in historical_data])
        df = df.drop('_sa_instance_state', axis=1, errors='ignore')

        # Calculate technical indicators
        df = calculate_technical_indicators(df)

        # Store the calculated indicators
        for _, row in df.iterrows():
            indicator = TechnicalIndicator(
                ticker_id=ticker.ticker_id,
                               date=row['date'],
                sma_20=row['sma_20'],
                rsi=row['rsi'],
                macd=row['macd'],
                bollinger_hband=row['bollinger_hband'],
                bollinger_lband=row['bollinger_lband']
            )
            db.add(indicator)

        db.commit()
        logger.info(f"Completed processing for ticker: {ticker.symbol}")

    logger.info("Feature engineering completed for all tickers")

def main():
    """
    Main function to process historical data and calculate technical indicators.
    """
    db = next(get_db())
    try:
        process_historical_data(db)
    except Exception as e:
        logger.error(f"An error occurred during feature engineering: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    main()