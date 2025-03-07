# api/prediction.py
"""
API endpoints for predictions
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional

from ml.prediction import make_prediction
from data.database import get_recent_predictions, get_prediction_history, update_actual_movements
from config import AVAILABLE_SYMBOLS

# Global variable from app.py
global_models = {}

router = APIRouter(tags=["predictions"])

@router.get("/api/predict/{symbol}")
async def predict_stock(symbol: str) -> Dict[str, Any]:
    """
    Get prediction for a stock's next-day movement
    """
    # Check if symbol is valid
    if symbol not in AVAILABLE_SYMBOLS:
        raise HTTPException(status_code=404, detail=f"Symbol {symbol} not supported")
    
    # Import here to avoid circular imports
    from app import global_models
    
    # Check if model exists
    if symbol not in global_models or global_models[symbol] is None:
        raise HTTPException(status_code=404, detail=f"No model available for {symbol}")
    
    # Make prediction
    try:
        result = make_prediction(global_models[symbol], symbol)
        if result is None:
            raise HTTPException(status_code=500, detail="Prediction failed")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.get("/api/predictions/recent")
async def get_recent(symbol: str, limit: int = Query(5, ge=1, le=20)) -> List[Dict[str, Any]]:
    """
    Get recent predictions for a symbol
    
    Args:
        symbol: Stock symbol
        limit: Maximum number of predictions to return
        
    Returns:
        List of recent predictions
    """
    # Check if symbol is valid
    if symbol not in AVAILABLE_SYMBOLS:
        raise HTTPException(status_code=404, detail=f"Symbol {symbol} not supported")
    
    return get_recent_predictions(symbol, limit)

@router.get("/api/predictions/history")
async def get_history(
    symbol: Optional[str] = None, 
    limit: int = Query(100, ge=1, le=500)
) -> List[Dict[str, Any]]:
    """
    Get prediction history
    
    Args:
        symbol: Optional stock symbol to filter by
        limit: Maximum number of predictions to return
        
    Returns:
        List of historical predictions
    """
    if symbol is not None and symbol not in AVAILABLE_SYMBOLS:
        raise HTTPException(status_code=404, detail=f"Symbol {symbol} not supported")
    
    return get_prediction_history(symbol, limit)

@router.post("/api/update-actual-movement")
async def update_movements() -> Dict[str, Any]:
    """
    Update actual movements for predictions
    
    Returns:
        Number of predictions updated
    """
    updated = update_actual_movements()
    return {"updated": updated}