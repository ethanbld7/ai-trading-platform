# ml/prediction.py
"""
Prediction logic for the ML models
"""
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

from data.stock_data import get_latest_data
from data.database import save_prediction
from ml.features import get_feature_list

def make_prediction(model_info: Dict[str, Any], symbol: str) -> Optional[Dict[str, Any]]:
    """
    Make a prediction for a stock's next-day movement
    
    Args:
        model_info: Dictionary with model and features
        symbol: Stock symbol
        
    Returns:
        Dictionary with prediction results or None if prediction fails
    """
    # Get latest data
    latest = get_latest_data(symbol)
    if latest is None:
        return None
    
    # Extract model and features
    model = model_info["model"]
    features = model_info["features"]
    
    try:
        # Extract feature values
        features_array = np.array([latest[f] for f in features]).reshape(1, -1)
        
        # Make prediction
        prediction = bool(model.predict(features_array)[0])
        confidence = float(model.predict_proba(features_array)[0][int(prediction)])
        
        # Create feature dict for storage
        feature_dict = {f: float(latest[f]) for f in features if f in latest}
        
        # Save prediction to database
        current_date = datetime.now()
        save_prediction(symbol, current_date, prediction, confidence, feature_dict)
        
        return {
            "symbol": symbol,
            "latest": latest,
            "prediction": {
                "movement": prediction,
                "confidence": confidence,
                "date": datetime.now().strftime("%Y-%m-%d")
            },
            "model_accuracy": model_info["accuracy"],
            "feature_importance": model_info["feature_importance"]
        }
    except Exception as e:
        print(f"Error making prediction: {e}")
        return None