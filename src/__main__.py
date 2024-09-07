# src/__main__.py
import sys
import asyncio
from src.data_collectors import financial_data_collector, historical_data_collector

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "financial":
            asyncio.run(financial_data_collector.main())
        elif sys.argv[1] == "historical":
            asyncio.run(historical_data_collector.main())
        else:
            print("Invalid argument. Use 'financial' or 'historical'.")
    else:
        print("Please specify which collector to run: 'financial' or 'historical'.")
