# src/database/models.py

CREATE_TABLES_QUERY = """
-- Tickers table
CREATE TABLE IF NOT EXISTS tickers (
    ticker_id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255),
    sector VARCHAR(255),
    industry VARCHAR(255)
);

-- Historical data table
CREATE TABLE IF NOT EXISTS historical_data (
    id SERIAL PRIMARY KEY,
    ticker_id INTEGER REFERENCES tickers(ticker_id),
    date DATE NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    adjusted_close NUMERIC,
    volume BIGINT,
    UNIQUE (ticker_id, date)
);

-- Minute data table
CREATE TABLE IF NOT EXISTS minute_data (
    ticker_id INTEGER REFERENCES tickers(ticker_id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    PRIMARY KEY (ticker_id, timestamp)
);

-- Financial data table
CREATE TABLE IF NOT EXISTS financial_data (
    id SERIAL PRIMARY KEY,
    ticker_id INTEGER REFERENCES tickers(ticker_id),
    date DATE NOT NULL,
    revenue NUMERIC,
    net_income NUMERIC,
    eps NUMERIC,
    total_assets NUMERIC,
    total_liabilities NUMERIC,
    total_equity NUMERIC,
    cash_flow_operating NUMERIC,
    cash_flow_investing NUMERIC,
    cash_flow_financing NUMERIC,
    UNIQUE (ticker_id, date)
);

-- News events table
CREATE TABLE IF NOT EXISTS news_events (
    id SERIAL PRIMARY KEY,
    ticker_id INTEGER REFERENCES tickers(ticker_id),
    event_date TIMESTAMP WITH TIME ZONE,
    event_type VARCHAR(255),
    description TEXT,
    source VARCHAR(255)
);

-- Analytics results table
CREATE TABLE IF NOT EXISTS analytics_results (
    id SERIAL PRIMARY KEY,
    ticker_id_1 INTEGER REFERENCES tickers(ticker_id),
    ticker_id_2 INTEGER REFERENCES tickers(ticker_id),
    correlation NUMERIC,
    timestamp TIMESTAMP WITH TIME ZONE
);
"""

async def create_tables():
    """Create database tables if they don't exist."""
    async with await get_db_connection() as conn:
        await conn.execute(CREATE_TABLES_QUERY)
