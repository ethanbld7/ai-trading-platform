# api/stock.py
"""
API endpoints for stock data
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from data.stock_data import get_data, format_stock_data_for_api

router = APIRouter(prefix="/api/stock", tags=["stock"])

@router.get("/{symbol}")
async def get_stock_data(symbol: str, period: str = "3m") -> List[Dict[str, Any]]:
    """
    Get historical stock data
    
    Args:
        symbol: Stock symbol
        period: Time period (1m, 3m, 6m, 1y)
        
    Returns:
        List of stock data points
    """
    # Map period to days
    period_days = {
        "1m": 30,
        "3m": 90,
        "6m": 180,
        "1y": 365
    }
    
    days = period_days.get(period, 90)
    
    # Get data
    df = get_data(symbol, period=period)
    if df is None:
        raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
    
    # Format for API response
    return format_stock_data_for_api(df, days)