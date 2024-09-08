# src/models/ticker.py

from sqlalchemy import Column, Integer, String
from src.database.db_utils import Base
from sqlalchemy.orm import relationship

class Ticker(Base):
    """
    SQLAlchemy model for the tickers table.
    """
    __tablename__ = "tickers"

    ticker_id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    sector = Column(String)
    industry = Column(String)
    technical_indicators = relationship("TechnicalIndicator", back_populates="ticker")