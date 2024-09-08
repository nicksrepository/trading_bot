# src/models/technical_indicators.py

from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db_utils import Base

class TechnicalIndicator(Base):
    __tablename__ = 'technical_indicators'

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey('tickers.ticker_id'), nullable=False)
    date = Column(Date, nullable=False)
    sma_20 = Column(Float)
    rsi = Column(Float)
    macd = Column(Float)
    bollinger_hband = Column(Float)
    bollinger_lband = Column(Float)
    
     # Relationship to the Ticker model
    ticker = relationship("Ticker", back_populates="technical_indicators")

    def __repr__(self):
        return f"<TechnicalIndicator(id={self.id}, ticker_id={self.ticker_id}, date={self.date})>"
