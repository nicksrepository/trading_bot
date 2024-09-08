# src/data_analysis/correlation_analysis.py

import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from src.database.db_utils import get_db
from src.models.ticker import Ticker
from src.utils.logging_config import setup_logging

logger = setup_logging("correlation_analysis")

async def perform_correlation_analysis():
    """
    Perform correlation analysis on historical data for all tickers.
    """
    db = next(get_db())
    try:
        # Fetch all tickers
        tickers = db.query(Ticker).all()
        
                # Fetch historical data for all tickers
        data = {}
        for ticker in tickers:
            query = f"""
            SELECT date, close 
            FROM historical_data 
            WHERE ticker_id = {ticker.ticker_id}
            ORDER BY date
            """
            df = pd.read_sql(query, db.bind)
            df.set_index('date', inplace=True)
            data[ticker.symbol] = df['close']
        
        # Combine all data into a single DataFrame
        all_data = pd.DataFrame(data)
        
        # Calculate correlation matrix
        correlation_matrix = all_data.corr()
        
                
        # Log some summary statistics
        logger.info(f"Correlation matrix shape: {correlation_matrix.shape}")
        logger.info(f"Average correlation: {correlation_matrix.values[np.triu_indices_from(correlation_matrix, k=1)].mean()}")
        
        # You might want to save this correlation matrix to a file or database
        correlation_matrix.to_csv('correlation_matrix.csv')
        
        logger.info("Correlation analysis completed successfully.")
    except Exception as e:
        logger.error(f"Error during correlation analysis: {e}")
    finally:
        db.close()

        