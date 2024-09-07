import yfinance as yf
import os
import pandas as pd
from time import sleep
import logging

# Define the path to the historical data folder
historical_folder = os.path.join('data', 'historical')

# Full list of tickers across various asset classes
tickers = [
    # US Treasuries
    '^IRX', '^FVX', '^TNX', '^TYX', '^US1M', '^US3M', '^US6M', '^US1Y', '^US2Y', '^US5Y', '^US10Y', '^US30Y',

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
    'BRK.B', 'AXP', 'BLK', 'SCHW', 'MMC', 'SPGI', 'MSCI', 'ICE', 'CME', 'MCO',

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

# Setup logging
def setup_logging():
    log_file = os.path.join('data', 'logs', 'data_ingestion.log')
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Log a message
def log_message(message, level='info'):
    if level == 'info':
        logging.info(message)
    elif level == 'warning':
        logging.warning(message)
    elif level == 'error':
        logging.error(message)
    print(message)

# Function to generate the correct file name for each ticker
def generate_file_name(ticker):
    if '=' in ticker:  # Currency pair format (e.g., 'CADUSD=X')
        return f'{ticker}_data.csv'
    else:  # Equity format (e.g., 'AAPL')
        return f'{ticker.lower()}_data.csv'

# Data integrity check
def check_data_integrity(df, ticker):
    all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='B')  # 'B' means business days
    missing_dates = all_dates.difference(df.index)
    
    if not missing_dates.empty:
        log_message(f"Warning: Missing dates detected in {ticker}: {missing_dates}", level='warning')

    # Check for duplicates
    if df.index.duplicated().any():
        log_message(f"Warning: Duplicate dates found in {ticker}. Dropping duplicates.", level='warning')
        df = df[~df.index.duplicated(keep='first')]
    
    return df

# Function to download and save historical data
def download_historical_data(ticker, start_date='2000-01-01', end_date=None):
    try:
        # Download data from Yahoo Finance
        data = yf.download(ticker, start=start_date, end=end_date)
        
        # Check if data was downloaded successfully
        if data.empty:
            log_message(f"No data found for {ticker}. Skipping.", level='warning')
            return
        
        # Define the file path for the CSV file
        file_name = generate_file_name(ticker)
        file_path = os.path.join(historical_folder, file_name)
        
        # Save data to CSV
        data.to_csv(file_path)
        log_message(f'Saved {ticker} data to {file_path}')
    
    except Exception as e:
        log_message(f"Error downloading data for {ticker}: {e}", level='error')

# Function to update existing data with new data
def update_historical_data(ticker):
    file_name = generate_file_name(ticker)
    file_path = os.path.join(historical_folder, file_name)
    
    if os.path.exists(file_path):
        # Load existing data
        existing_data = pd.read_csv(file_path, index_col='Date', parse_dates=True)
        
        # Check data integrity
        existing_data = check_data_integrity(existing_data, ticker)
        
        last_date = existing_data.index[-1]
        
        # Download new data starting from the last available date
        new_data = yf.download(ticker, start=last_date + pd.Timedelta(days=1))
        
        if not new_data.empty:
            # Append new data and save
            updated_data = existing_data.append(new_data)
            updated_data.to_csv(file_path)
            log_message(f"Updated {ticker} data in {file_path}")
        else:
            log_message(f"No new data available for {ticker}.", level='info')
    
    else:
        # If the file doesn't exist, download the full dataset
        download_historical_data(ticker)

# Main function to run the data ingestion process
def main():
    setup_logging()
    
    # Ensure the historical folder exists
    os.makedirs(historical_folder, exist_ok=True)
    
    # Download or update data for each ticker with a delay to avoid rate limiting
    for ticker in tickers:
        log_message(f"Processing ticker: {ticker}")
        update_historical_data(ticker)
        sleep(1)  # Add a short delay to avoid hitting API rate limits

if __name__ == "__main__":
    main()

