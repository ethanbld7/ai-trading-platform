
"""
Configuration settings for the AI Trading Platform
"""
import os
from typing import List

# Database settings
DB_NAME = os.getenv("DB_NAME", "finance_data")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Available stock symbols
AVAILABLE_SYMBOLS: List[str] = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", 
    "TSLA", "NVDA", "JPM", "V", "WMT", "JNJ"
]

# Initial symbols to load at startup
INITIAL_SYMBOLS: List[str] = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

# ML Model parameters
MODEL_PARAMS = {
    "n_estimators": 100,
    "learning_rate": 0.1,
    "max_depth": 6,
    "min_child_weight": 1,
    "gamma": 0,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "objective": 'binary:logistic',
    "random_state": 42
}

# Portfolio simulation defaults
DEFAULT_INITIAL_BALANCE = 10000
DEFAULT_SIMULATION_DAYS = 90

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8000

# Updates
MODEL_UPDATE_INTERVAL = 24 * 60 * 60  # 24 hours in seconds