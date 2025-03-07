# api/portfolio.py
"""
API endpoints for portfolio simulation
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any

from services.portfolio import simulate_portfolio
from config import AVAILABLE_SYMBOLS, DEFAULT_INITIAL_BALANCE, DEFAULT_SIMULATION_DAYS

router = APIRouter(tags=["portfolio"])

@router.get("/api/portfolio/simulate")
async def simulate(
    symbol: str,
    days: int = Query(DEFAULT_SIMULATION_DAYS, ge=30, le=365),
    initial_balance: float = Query(DEFAULT_INITIAL_BALANCE, ge=1000, le=1000000)
) -> Dict[str, Any]:
    """
    Run a portfolio simulation
    
    Args:
        symbol: Stock symbol
        days: Number of days to simulate
        initial_balance: Initial portfolio balance
        
    Returns:
        Simulation results
    """
    # Check if symbol is valid
    if symbol not in AVAILABLE_SYMBOLS:
        raise HTTPException(status_code=404, detail=f"Symbol {symbol} not supported")
    
    # Run simulation
    result = simulate_portfolio(symbol, days, initial_balance)
    if result is None:
        raise HTTPException(status_code=500, detail="Simulation failed")
    
    return result