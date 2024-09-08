# src/config.py

import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

#FINANCIAL_DATA_YEARS = 5

# Database configuration
"""DB_HOST = "localhost"
DB_NAME = "trading_bot_db"
DB_USER = "postgres"
DB_PASSWORD = "dildobaggins" """

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "trading_bot_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Paths
"""BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
HISTORICAL_DATA_DIR = os.path.join(DATA_DIR, 'historical')
MINUTE_DATA_DIR = os.path.join(DATA_DIR, 'minute_data')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Ensure directories exist
for directory in [DATA_DIR, HISTORICAL_DATA_DIR, MINUTE_DATA_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

# API configuration
CONCURRENCY_LIMIT = 10
BATCH_SIZE = 1000

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Tickers list (you can keep the existing list here)
TICKERS = [
        # US Treasuries

    # Major Bank Stocks
    'JPM', 'BAC', 'C', 'WFC', 'GS', 'MS', 'USB', 'PNC', 'BK', 'STT',

    # Energy Commodities
    'CL=F', 'BZ=F', 'NG=F', 'RB=F', 'HO=F',

    # Large Oil Companies
    'XOM', 'CVX', 'BP', 'RDS.A', 'TOT',

    # Defense Stocks
    'LMT', 'NOC', 'GD', 'RTN', 'BA', 'HII', 'TXT', 'HON', 'GD', 'LHX',

    # Tech Stocks
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'NVDA', 'INTC', 'CSCO', 'ORCL',

    # Healthcare Stocks
    'JNJ', 'PFE', 'MRK', 'ABT', 'LLY', 'BMY', 'GILD', 'AMGN', 'ZTS', 'BIIB',

    # Consumer Goods Stocks
    'PG', 'KO', 'PEP', 'MO', 'PM', 'CL', 'KMB', 'MDLZ', 'UL', 'NWL',

    # Utilities Stocks
    'NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'SRE', 'PCG', 'PEG', 'XEL',

    # Industrial Stocks
    'GE', 'MMM', 'CAT', 'BA', 'HON', 'UTX', 'LMT', 'GD', 'NOC', 'RTN',

    # Financial Stocks
    'AXP', 'BLK', 'SCHW', 'MMC', 'SPGI', 'MSCI', 'ICE', 'CME', 'MCO',

    # Real Estate Stocks
    'AMT', 'PLD', 'CCI', 'EQIX', 'PSA', 'SPG', 'AVB', 'EQR', 'ESS', 'O',

    # Penny Stocks
    'SIRI', 'FCEL', 'PLUG', 'IDEX', 'GPRO', 'BB', 'NOK', 'FUBO', 'VIVE', 'OCGN',

    # Transportation Stocks
    'UPS', 'FDX', 'DAL', 'UAL', 'LUV', 'JBHT', 'EXPD', 'CHRW', 'XPO', 'NSC',

    # Retail Stocks
    'WMT', 'TGT', 'COST', 'AMZN', 'BBY', 'HD', 'LOW', 'M', 'KSS', 'TJX',

    # Telecom Stocks
    'VZ', 'T', 'TMUS', 'S', 'CHL', 'VOD', 'ORAN', 'NOK', 'ERIC', 'AMX',

    # Energy ETFs
    'XLE', 'XOP', 'OIH', 'VDE', 'IXC', 'ERX', 'ERY', 'PXI', 'IYE', 'FENY',

    # Gold and Metals
    'GLD', 'SLV', 'PPLT', 'PALL', 'GDX', 'GDXJ', 'IAU', 'DBP', 'SGOL', 'RING',

    # S&P 500 Index and Major Indices
    'SPY', 'DIA', 'QQQ', 'IWM', 'IVV', 'VOO', 'VTI', 'VTV', 'MTUM', 'SCHX',

    # Technology ETFs
    'XLK', 'VGT', 'FTEC', 'IYW', 'RYT', 'IXN', 'IGM', 'QTEC', 'XSD', 'SOXX',

    # Utilities ETFs
    'XLU', 'VPU', 'IDU', 'FUTY', 'RYU', 'PUI', 'FXU', 'JXI', 'PUI', 'RYU',

    # Dividend ETFs
    'VYM', 'DVY', 'SDY', 'HDV', 'SCHD', 'NOBL', 'VIG', 'SPYD', 'FVD', 'DLN',

    # Additional Major Sectors
    'XLF', 'XLI', 'XLY', 'XLP', 'XLV', 'XLB', 'XLRE', 'XTL', 'XLU', 'XLK'
]

# Add this line at the end of the file
if __name__ == "__main__":
    print("Configuration loaded successfully.")
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"DB_HOST: {DB_HOST}")
    print(f"DB_NAME: {DB_NAME}")

"""
# API configuration
CONCURRENCY_LIMIT = int(os.getenv("CONCURRENCY_LIMIT", 10))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 1000))

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Ensure directories exist
for directory in [DATA_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

# Tickers list
TICKERS = [
  # US Treasuries

    # Major Bank Stocks
    'JPM', 'BAC', 'C', 'WFC', 'GS', 'MS', 'USB', 'PNC', 'BK', 'STT',

    # Energy Commodities
    'CL=F', 'BZ=F', 'NG=F', 'RB=F', 'HO=F',

    # Large Oil Companies
    'XOM', 'CVX', 'BP', 'RDS.A', 'TOT',

    # Defense Stocks
    'LMT', 'NOC', 'GD', 'RTN', 'BA', 'HII', 'TXT', 'HON', 'GD', 'LHX',

    # Tech Stocks
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'NVDA', 'INTC', 'CSCO', 'ORCL',

    # Healthcare Stocks
    'JNJ', 'PFE', 'MRK', 'ABT', 'LLY', 'BMY', 'GILD', 'AMGN', 'ZTS', 'BIIB',

    # Consumer Goods Stocks
    'PG', 'KO', 'PEP', 'MO', 'PM', 'CL', 'KMB', 'MDLZ', 'UL', 'NWL',

    # Utilities Stocks
    'NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'SRE', 'PCG', 'PEG', 'XEL',

    # Industrial Stocks
    'GE', 'MMM', 'CAT', 'BA', 'HON', 'UTX', 'LMT', 'GD', 'NOC', 'RTN',

    # Financial Stocks
    'AXP', 'BLK', 'SCHW', 'MMC', 'SPGI', 'MSCI', 'ICE', 'CME', 'MCO',

    # Real Estate Stocks
    'AMT', 'PLD', 'CCI', 'EQIX', 'PSA', 'SPG', 'AVB', 'EQR', 'ESS', 'O',

    # Penny Stocks
    'SIRI', 'FCEL', 'PLUG', 'IDEX', 'GPRO', 'BB', 'NOK', 'FUBO', 'VIVE', 'OCGN',

    # Transportation Stocks
    'UPS', 'FDX', 'DAL', 'UAL', 'LUV', 'JBHT', 'EXPD', 'CHRW', 'XPO', 'NSC',

    # Retail Stocks
    'WMT', 'TGT', 'COST', 'AMZN', 'BBY', 'HD', 'LOW', 'M', 'KSS', 'TJX',

    # Telecom Stocks
    'VZ', 'T', 'TMUS', 'S', 'CHL', 'VOD', 'ORAN', 'NOK', 'ERIC', 'AMX',

    # Energy ETFs
    'XLE', 'XOP', 'OIH', 'VDE', 'IXC', 'ERX', 'ERY', 'PXI', 'IYE', 'FENY',

    # Gold and Metals
    'GLD', 'SLV', 'PPLT', 'PALL', 'GDX', 'GDXJ', 'IAU', 'DBP', 'SGOL', 'RING',

    # S&P 500 Index and Major Indices
    'SPY', 'DIA', 'QQQ', 'IWM', 'IVV', 'VOO', 'VTI', 'VTV', 'MTUM', 'SCHX',

    # Technology ETFs
    'XLK', 'VGT', 'FTEC', 'IYW', 'RYT', 'IXN', 'IGM', 'QTEC', 'XSD', 'SOXX',

    # Utilities ETFs
    'XLU', 'VPU', 'IDU', 'FUTY', 'RYU', 'PUI', 'FXU', 'JXI', 'PUI', 'RYU',

    # Dividend ETFs
    'VYM', 'DVY', 'SDY', 'HDV', 'SCHD', 'NOBL', 'VIG', 'SPYD', 'FVD', 'DLN',

    # Additional Major Sectors
    'XLF', 'XLI', 'XLY', 'XLP', 'XLV', 'XLB', 'XLRE', 'XTL', 'XLU', 'XLK'
]






