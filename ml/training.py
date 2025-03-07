# ml/training.py
"""
Model training functionality
"""
import xgboost as xgb
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from sklearn.metrics import accuracy_score

from data.stock_data import get_data
from ml.features import prepare_training_data, split_data, get_feature_list
from config import MODEL_PARAMS

def train_model(symbol: str) -> Optional[Dict[str, Any]]:
    """
    Train an XGBoost model for the given stock symbol
    
    Args:
        symbol: Stock symbol
        
    Returns:
        Dictionary with model, accuracy, feature importance, and features list
        or None if training fails
    """
    # Get stock data
    df = get_data(symbol)
    if df is None:
        print(f"No data found for {symbol}")
        return None

    # Prepare data for training
    df, features = prepare_training_data(df)
    if features is None:
        return None
        
    # Train/Test Split
    X_train, X_test, y_train, y_test = split_data(df, features)

    # Ensure we have enough data after the split
    if X_train.shape[0] < 20:
        print("Not enough data for training.")
        return None

    try:
        # Train Model
        model = xgb.XGBClassifier(**MODEL_PARAMS)
        model.fit(X_train, y_train)

        # Evaluate Model
        preds = model.predict(X_test)
        accuracy = accuracy_score(y_test, preds)
        print(f"Model Accuracy for {symbol}: {accuracy:.4f}")

        # Save feature importance
        feature_importance = {
            "features": features,
            "importance": model.feature_importances_.tolist()
        }
        
        return {
            "model": model,
            "accuracy": accuracy,
            "feature_importance": feature_importance,
            "features": features
        }
    except Exception as e:
        print(f"Error training model: {e}")
        return None

def get_feature_importance(model_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract feature importance from a trained model
    
    Args:
        model_info: Dictionary with model information
        
    Returns:
        Dictionary with feature importance information
    """
    return model_info["feature_importance"]