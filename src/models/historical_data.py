# src/models/historical_data.py
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from src.database.db_utils import Base

class HistoricalData(Base):
    __tablename__ = 'historical_data'

    id = Column(Integer, primary_key=True)
    ticker_id = Column(Integer, ForeignKey('tickers.ticker_id'))
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

# src/models/technical_indicators.py
from sqlalchemy import Column, Integer, String, Date, Float
from src.database.db_utils import Base

class TechnicalIndicator(Base):
    __tablename__ = 'technical_indicators'

    id = Column(Integer, primary_key=True)
    ticker_id = Column(Integer, ForeignKey('tickers.ticker_id'))
    date = Column(Date)
    sma_20 = Column(Float)
    rsi = Column(Float)
    macd = Column(Float)
    bollinger_hband = Column(Float)
    bollinger_lband = Column(Float)