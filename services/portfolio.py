# services/portfolio.py
"""
Portfolio simulation functionality
"""
import pandas as pd
import numpy as np
import xgboost as xgb
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from data.stock_data import get_data
from data.database import save_portfolio_simulation
from ml.features import add_features, get_feature_list

def simulate_portfolio(symbol: str, days: int = 90, initial_balance: float = 10000) -> Optional[Dict[str, Any]]:
    """
    Run a portfolio simulation based on a trained model
    
    Args:
        symbol: Stock symbol
        days: Number of days to simulate
        initial_balance: Initial portfolio balance
        
    Returns:
        Dictionary with simulation results or None if simulation fails
    """
    # Get historical data for simulation period
    df = get_data(symbol, period="1y")
    if df is None or len(df) < days:
        return None
        
    # Only use the last X days for simulation
    df = df.tail(days).copy()
    
    # Get data for model training (data before simulation period)
    model_data = get_data(symbol, period="2y")
    if model_data is None:
        return None
        
    # Find cutoff date (start of simulation)
    cutoff_date = df.iloc[0]["date"]
    
    # Use only data before simulation for training
    training_data = model_data[model_data["date"] < cutoff_date].copy()
    
    # Add features to both datasets
    training_data = add_features(training_data)
    df = add_features(df)
    
    # Add target for training data
    training_data["target"] = (training_data["close_price"].shift(-1) > training_data["close_price"]).astype(int)
    df["target"] = (df["close_price"].shift(-1) > df["close_price"]).astype(int)
    
    # Drop missing values
    training_data = training_data.dropna()
    df = df.dropna()
    
    if len(training_data) < 30:
        return None
        
    # Get features for prediction
    features = get_feature_list()
    
    # Train the model on historical data
    model = xgb.XGBClassifier(random_state=42)
    model.fit(training_data[features], training_data["target"])
    
    # Run simulation
    balance = initial_balance
    shares = 0
    trades = []
    daily_balance = []
    
    for i in range(len(df) - 1):  # -1 because we need the next day's price
        current_data = df.iloc[i]
        next_data = df.iloc[i + 1]
        
        # Make prediction
        features_array = current_data[features].values.reshape(1, -1)
        prediction = model.predict(features_array)[0]
        confidence = model.predict_proba(features_array)[0][prediction]
        
        # Decision based on prediction
        if prediction == 1 and shares == 0:  # Predict price will go up -> Buy
            # Buy shares
            shares = balance / current_data["close_price"]
            trade_cost = shares * current_data["close_price"]
            balance = 0
            
            trades.append({
                "date": current_data["date"].strftime("%Y-%m-%d") if isinstance(current_data["date"], pd.Timestamp) else str(current_data["date"]),
                "action": "BUY",
                "price": float(current_data["close_price"]),
                "shares": float(shares),
                "value": float(trade_cost),
                "confidence": float(confidence)
            })
        
        elif prediction == 0 and shares > 0:  # Predict price will go down -> Sell
            # Sell shares
            trade_value = shares * current_data["close_price"]
            balance = trade_value
            
            trades.append({
                "date": current_data["date"].strftime("%Y-%m-%d") if isinstance(current_data["date"], pd.Timestamp) else str(current_data["date"]),
                "action": "SELL",
                "price": float(current_data["close_price"]),
                "shares": float(shares),
                "value": float(trade_value),
                "confidence": float(confidence)
            })
            
            shares = 0
        
        # Calculate total value for this day
        total_value = balance + (shares * current_data["close_price"])
        
        daily_balance.append({
            "date": current_data["date"].strftime("%Y-%m-%d") if isinstance(current_data["date"], pd.Timestamp) else str(current_data["date"]),
            "balance": float(total_value),
            "shares": float(shares),
            "price": float(current_data["close_price"])
        })
    
    # Final day
    final_day = df.iloc[-1]
    final_balance = balance + (shares * final_day["close_price"])
    
    # If we still have shares, sell them at the end
    if shares > 0:
        trades.append({
            "date": final_day["date"].strftime("%Y-%m-%d") if isinstance(final_day["date"], pd.Timestamp) else str(final_day["date"]),
            "action": "FINAL SELL",
            "price": float(final_day["close_price"]),
            "shares": float(shares),
            "value": float(shares * final_day["close_price"]),
            "confidence": 1.0
        })
    
    # Calculate buy & hold strategy
    buy_and_hold_shares = initial_balance / df.iloc[0]["close_price"]
    buy_and_hold_final = buy_and_hold_shares * final_day["close_price"]
    
    # Add final daily balance
    daily_balance.append({
        "date": final_day["date"].strftime("%Y-%m-%d") if isinstance(final_day["date"], pd.Timestamp) else str(final_day["date"]),
        "balance": float(final_balance),
        "shares": float(shares),
        "price": float(final_day["close_price"])
    })
    
    # Create result dictionary
    result = {
        "initial_balance": initial_balance,
        "final_balance": final_balance,
        "roi_percentage": ((final_balance / initial_balance) - 1) * 100,
        "trades": trades,
        "daily_balance": daily_balance,
        "buy_and_hold": {
            "initial_balance": initial_balance,
            "final_balance": buy_and_hold_final,
            "roi_percentage": ((buy_and_hold_final / initial_balance) - 1) * 100
        },
        "symbol": symbol,
        "days": days
    }
    
    # Save simulation results to database
    save_portfolio_simulation(
        datetime.now() - timedelta(days=days),
        datetime.now(),
        initial_balance,
        final_balance,
        result["roi_percentage"],
        trades
    )
    
    return result