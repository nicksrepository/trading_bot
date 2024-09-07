import yfinance as yf
import pandas as pd
from datetime import datetime

# Define date range
start_date = '2000-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')

# List of tickers covering a wide range of sectors, including 50 currencies
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
    'XLF', 'XLI', 'XLY', 'XLP', 'XLV', 'XLB', 'XLRE', 'XTL', 'XLU', 'XLK',

    # Major Currencies (50 Currencies)
    'EURUSD=X', 'JPYUSD=X', 'GBPUSD=X', 'AUDUSD=X', 'NZDUSD=X', 'CADUSD=X', 'CHFUSD=X', 'CNYUSD=X', 'RUBUSD=X',
    'INRUSD=X', 'BRLUSD=X', 'ZARUSD=X', 'MXNUSD=X', 'KRWUSD=X', 'SGDUSD=X', 'HKDUSD=X', 'TRYUSD=X', 'IDRUSD=X',
    'MYRUSD=X', 'PHPUSD=X', 'THBUSD=X', 'VNDUSD=X', 'TWDUSD=X', 'SARUSD=X', 'ILSUSD=X', 'NGNUSD=X', 'EGPUSD=X',
    'CLPUSD=X', 'PENUSD=X', 'COPUSD=X', 'VEFUSD=X', 'ARSUSD=X', 'BOBUSD=X', 'UYUUSD=X', 'PYGUSD=X', 'HUFUSD=X',
    'CZKUSD=X', 'PLNUSD=X', 'RONUSD=X', 'BGNUSD=X', 'HRKUSD=X', 'DKKUSD=X', 'NOKUSD=X', 'SEKUSD=X', 'ISKUSD=X',
    'UAHUSD=X', 'BYNUSD=X', 'GHSUSD=X', 'KESUSD=X', 'TNDUSD=X', 'MADUSD=X'
]

# Download historical data for all tickers
data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')

# Save each ticker's data to a separate CSV file
for ticker in tickers:
    data[ticker].to_csv(f'{ticker}_data.csv')

print("Download complete. Data has been saved to CSV files.")
