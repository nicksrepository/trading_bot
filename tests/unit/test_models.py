# tests/unit/test_models.py

import pytest
from src.models.pydantic_models import Ticker, HistoricalData

def test_ticker_model():
    ticker_data = {
        "ticker_id": 1,
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics"
    }
    ticker = Ticker(**ticker_data)
    assert ticker.ticker_id == 1
    assert ticker.symbol == "AAPL"
    assert ticker.name == "Apple Inc."
    assert ticker.sector == "Technology"
    assert ticker.industry == "Consumer Electronics"
    
def test_historical_data_model():
    historical_data = {
        "id": 1,
        "ticker_id": 1,
        "date": "2023-04-14",
        "open": 100.0,
        "high": 101.0,
        "low": 99.0,
        "close": 100.5,
        "volume": 1000000
    }
    data = HistoricalData(**historical_data)
    assert data.id == 1
    assert data.ticker_id == 1
    assert data.date.isoformat() == "2023-04-14"
    assert data.open == 100.0
    assert data.high == 101.0
    assert data.low == 99.0
    assert data.close == 100.5
    assert data.volume == 1000000