# data/stock_data.py
"""
Stock data fetching and processing functionality
"""
import yfinance as yf
import pandas as pd
from typing import Optional, Dict, Any, Union, List
import numpy as np

from data.database import get_stock_data, save_stock_data, connect_db

def fetch_stock_data(symbol="AAPL"):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="2y")  # Get 2 years of data for better training
        if df.empty:
            print(f"No data found for symbol {symbol}")
            return False
            
        df.reset_index(inplace=True)

        conn = connect_db()
        if conn is None:
            return False
            
        cursor = conn.cursor()
        
        # First clear existing data for this symbol
        cursor.execute("DELETE FROM stock_prices WHERE symbol = %s", (symbol,))
        
        for _, row in df.iterrows():
            cursor.execute(
                """INSERT INTO stock_prices 
                   (symbol, date, open_price, close_price, high_price, low_price, volume, adjusted_close) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (symbol, row["Date"], row["Open"], row["Close"], 
                 row["High"], row["Low"], row["Volume"], 
                 row["Close"] if "Adj Close" not in row else row["Adj Close"])
            )

        conn.commit()
        conn.close()
        print(f"Stock data for {symbol} stored in database.")
        return True
    except Exception as e:
        print(f"Error fetching stock data for {symbol}: {e}")
        return False

def get_data(symbol: str, from_db: bool = True, period: str = "2y") -> Optional[pd.DataFrame]:
    """
    Get stock data from database or yfinance if not available
    
    Args:
        symbol: Stock symbol
        from_db: Whether to try the database first
        period: Time period for yfinance (if needed)
    
    Returns:
        DataFrame with stock data or None if unavailable
    """
    # Try database first if requested
    if from_db:
        df = get_stock_data(symbol)
        if df is not None and not df.empty:
            return df
    
    # Fallback to yfinance
    return get_external_stock_data(symbol, period)

def get_external_stock_data(symbol: str, period: str = "3mo") -> Optional[pd.DataFrame]:
    """
    Get stock data directly from yfinance with correct period format
    """
    # Convert web API period format to yfinance format
    period_mapping = {
        "1m": "1mo",
        "3m": "3mo", 
        "6m": "6mo",
        "1y": "1y"
    }
    
    # Use mapped period or default to "3mo" if not found
    yf_period = period_mapping.get(period, "3mo")
    
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=yf_period)
        
        if df.empty:
            return None
            
        df.reset_index(inplace=True)
        df['symbol'] = symbol
        
        # Make sure column names match exactly
        df = df.rename(columns={
            "Date": "date", 
            "Open": "open_price", 
            "Close": "close_price", 
            "High": "high_price",
            "Low": "low_price",
            "Volume": "volume"
        })
        
        # Add adjusted close
        if "Adj Close" in df.columns:
            df = df.rename(columns={"Adj Close": "adjusted_close"})
        else:
            df["adjusted_close"] = df["close_price"]
            
        return df
    except Exception as e:
        print(f"{symbol}: {str(e)}")
        return None

def get_latest_data(symbol: str) -> Optional[Dict[str, Any]]:
    """
    Get latest stock data with engineered features
    
    Args:
        symbol: Stock symbol
    
    Returns:
        Dictionary with latest data and features or None
    """
    try:
        # Get enough days to calculate features
        stock = yf.Ticker(symbol)
        df = stock.history(period="60d")
        
        if df.empty:
            return None
        
        df.reset_index(inplace=True)
        df = df.rename(columns={
            "Date": "date", 
            "Open": "open_price", 
            "Close": "close_price", 
            "High": "high_price",
            "Low": "low_price",
            "Volume": "volume"
        })
        
        # Add features (same as in ml/features.py)
        from ml.features import add_features
        df = add_features(df)
        
        # Get the most recent data
        latest = df.iloc[-1].to_dict()
        
        # Add formatted date for display
        if isinstance(latest["date"], pd.Timestamp):
            latest["formatted_date"] = latest["date"].strftime("%Y-%m-%d")
        else:
            latest["formatted_date"] = str(latest["date"])
            
        # Format values for display
        for key in latest:
            if isinstance(latest[key], (float, np.float64)):
                latest[key] = float(latest[key])
                
        return latest
    except Exception as e:
        print(f"Error fetching latest data: {e}")
        return None

# Add this function to data/stock_data.py or update if it exists
def format_stock_data_for_api(df: pd.DataFrame, days: int = 90) -> List[Dict[str, Any]]:
    """
    Format stock data for API response, with column name validation
    """
    data = []
    for _, row in df.iterrows():
        # Create item with safe column access
        item = {
            "date": row["date"].strftime("%Y-%m-%d") if isinstance(row["date"], pd.Timestamp) else str(row["date"]),
            "open_price": float(row["open_price"]) if "open_price" in row else 0.0,
            "close_price": float(row["close_price"]) if "close_price" in row else 0.0,
            "volume": int(row["volume"]) if "volume" in row else 0
        }
        
        # Add optional fields if they exist
        if "high_price" in row:
            item["high_price"] = float(row["high_price"])
        else:
            item["high_price"] = item["close_price"]  # Use close price as fallback
            
        if "low_price" in row:
            item["low_price"] = float(row["low_price"])
        else:
            item["low_price"] = item["close_price"]  # Use close price as fallback
            
        data.append(item)
    
    # Keep only the most recent data based on days
    return data[-days:]