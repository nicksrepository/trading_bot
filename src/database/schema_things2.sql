SELECT * FROM historical_data WHERE ticker_id = (SELECT ticker_id FROM tickers WHERE symbol = 'AAPL');
