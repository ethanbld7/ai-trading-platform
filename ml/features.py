# ml/features.py
"""
Feature engineering for ML models
"""
import pandas as pd
from typing import List, Tuple, Dict, Any, Optional

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add engineered features to the dataframe
    
    Args:
        df: DataFrame with stock data
        
    Returns:
        DataFrame with additional features
    """
    # Make a copy to avoid modifying the original
    df = df.copy()
    
    # Price change features
    df["price_change"] = df["close_price"].pct_change()
    df["volatility"] = df["price_change"].rolling(window=5).std()
    
    # Moving averages
    df["ma5"] = df["close_price"].rolling(window=5).mean()
    df["ma20"] = df["close_price"].rolling(window=20).mean()
    df["ma50"] = df["close_price"].rolling(window=50).mean()
    
    # Price relative to moving averages
    df["price_rel_ma5"] = df["close_price"] / df["ma5"] - 1
    df["price_rel_ma20"] = df["close_price"] / df["ma20"] - 1
    df["price_rel_ma50"] = df["close_price"] / df["ma50"] - 1
    
    # Volume features
    df["volume_change"] = df["volume"].pct_change()
    df["avg_volume_5d"] = df["volume"].rolling(window=5).mean()
    df["volume_rel_avg"] = df["volume"] / df["avg_volume_5d"] - 1
    
    # Price range
    df["day_range"] = (df["high_price"] - df["low_price"]) / df["open_price"]
    
    return df

def prepare_training_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[List[str]]]:
    """
    Prepare data for model training
    
    Args:
        df: DataFrame with stock data
        
    Returns:
        DataFrame with features and target, list of feature names
    """
    # Add engineered features
    df = add_features(df)
    
    # Add target: Next day's movement (1 for up, 0 for down)
    df["target"] = (df["close_price"].shift(-1) > df["close_price"]).astype(int)
    
    # Drop missing values
    df = df.dropna()
    
    # Check if there is enough data
    if df.shape[0] < 30:  # Ensure we have enough rows
        print("Not enough data after feature engineering.")
        return df, None
    
    return df, get_feature_list()

def get_feature_list() -> List[str]:
    """
    Get the list of features used for prediction
    
    Returns:
        List of feature names
    """
    return [
        "open_price", "close_price", "high_price", "low_price", "volume",
        "volatility", "price_change", "price_rel_ma5", "price_rel_ma20", 
        "price_rel_ma50", "volume_change", "volume_rel_avg", "day_range"
    ]

def split_data(df: pd.DataFrame, features: List[str], target_col: str = "target") -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split data into training and testing sets
    
    Args:
        df: DataFrame with features and target
        features: List of feature column names
        target_col: Target column name
        
    Returns:
        X_train, X_test, y_train, y_test
    """
    from sklearn.model_selection import train_test_split
    
    X_train, X_test, y_train, y_test = train_test_split(
        df[features], df[target_col], test_size=0.2, random_state=42
    )
    
    return X_train, X_test, y_train, y_test