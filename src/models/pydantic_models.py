# src/models/pydantic_models.py

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class TickerBase(BaseModel):
    symbol: str
    name: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None

class TickerCreate(TickerBase):
    pass

class Ticker(TickerBase):
    ticker_id: int

    class Config:
        orm_mode = True

class HistoricalDataBase(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int

class HistoricalDataCreate(HistoricalDataBase):
    ticker_id: int

class HistoricalData(HistoricalDataBase):
    id: int
    ticker_id: int

    class Config:
        orm_mode = True