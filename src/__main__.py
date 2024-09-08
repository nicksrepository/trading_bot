
# src/main.py

import sys
import asyncio
from src.data_collectors.financial_data_collector import collect_financial_data
from src.data_collectors.historical_data_collector import collect_historical_data
from src.data_processors.data_cleaner import clean_data
from src.data_processors.feature_engineering import engineer_features
from src.data_analysis.correlation_analysis import perform_correlation_analysis
from src.utils.logging_config import setup_logging

logger = setup_logging("main")

async def main():
    logger.info("Starting data collection and processing pipeline")

    # Collect data
    await collect_financial_data()
    await collect_historical_data()


    # Process data
    await clean_data()
    await engineer_features()

    # Analyze data
    await perform_correlation_analysis()

    logger.info("Data collection and processing pipeline completed")

if __name__ == "__main__":
    asyncio.run(main())