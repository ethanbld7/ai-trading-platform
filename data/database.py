# data/database.py
"""
Database connection and operations for the AI Trading Platform
"""
import psycopg2
import pandas as pd
from typing import Optional, Dict, Any, List, Tuple
import json
from datetime import datetime

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def connect_db():
    """
    Create a connection to the PostgreSQL database
    
    Returns:
        Connection object or None if connection fails
    """
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            sslmode="disable"
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None

def create_tables():
    conn = connect_db()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    # Drop tables if they exist to ensure clean schema
    cursor.execute("DROP TABLE IF EXISTS stock_prices CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS prediction_history CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS portfolio_simulation CASCADE;")
    
    # Create stock_prices table with correct column names
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10),
            date TIMESTAMP,
            open_price FLOAT,
            close_price FLOAT,
            high_price FLOAT,  
            low_price FLOAT,
            volume INT,
            adjusted_close FLOAT
        );
    """)
    
    # Create a table for model predictions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10),
            prediction_date TIMESTAMP,
            predicted_movement BOOLEAN,
            confidence FLOAT,
            actual_movement BOOLEAN NULL,
            features JSON
        );
    """)
    
    # Create a table for portfolio simulation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio_simulation (
            id SERIAL PRIMARY KEY,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            initial_balance FLOAT,
            final_balance FLOAT,
            roi FLOAT,
            trades JSON,
            strategy VARCHAR(50)
        );
    """)
    
    conn.commit()
    conn.close()
    return True

def save_stock_data(symbol: str, data: pd.DataFrame) -> bool:
    """
    Save stock data to the database
    
    Args:
        symbol: Stock symbol
        data: DataFrame with stock data
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = connect_db()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    
    # First clear existing data for this symbol
    cursor.execute("DELETE FROM stock_prices WHERE symbol = %s", (symbol,))
    
    # Insert new data
    for _, row in data.iterrows():
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
    return True

def get_stock_data(symbol: str) -> Optional[pd.DataFrame]:
    """
    Retrieve stock data from the database
    
    Args:
        symbol: Stock symbol
    
    Returns:
        DataFrame with stock data or None if retrieval fails
    """
    try:
        conn = connect_db()
        if conn is None:
            return None
            
        query = f"SELECT * FROM stock_prices WHERE symbol='{symbol}' ORDER BY date"
        df = pd.read_sql(query, conn)
        conn.close()
        
        if not df.empty:
            return df
        return None
    except Exception as e:
        print(f"Error retrieving data from database: {e}")
        return None

def save_prediction(
    symbol: str, 
    prediction_date: datetime, 
    predicted_movement: bool, 
    confidence: float, 
    features: Dict[str, float]
) -> bool:
    """
    Save a prediction to the database
    
    Args:
        symbol: Stock symbol
        prediction_date: Date of the prediction
        predicted_movement: True for up, False for down
        confidence: Prediction confidence (0-1)
        features: Feature values used for prediction
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = connect_db()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """INSERT INTO prediction_history 
               (symbol, prediction_date, predicted_movement, confidence, features) 
               VALUES (%s, %s, %s, %s, %s)""",
            (symbol, prediction_date, predicted_movement, confidence, json.dumps(features))
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving prediction: {e}")
        conn.close()
        return False

def get_recent_predictions(symbol: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get recent predictions for a symbol
    
    Args:
        symbol: Stock symbol
        limit: Maximum number of predictions to return
    
    Returns:
        List of prediction dictionaries
    """
    conn = connect_db()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, symbol, prediction_date, predicted_movement, confidence, actual_movement
           FROM prediction_history 
           WHERE symbol = %s
           ORDER BY prediction_date DESC
           LIMIT %s""",
        (symbol, limit)
    )
    
    predictions = []
    for row in cursor.fetchall():
        predictions.append({
            "id": row[0],
            "symbol": row[1],
            "date": row[2].strftime("%Y-%m-%d"),
            "predicted_movement": row[3],
            "confidence": row[4],
            "actual_movement": row[5]
        })
    
    conn.close()
    return predictions

def get_prediction_history(symbol: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Get prediction history
    
    Args:
        symbol: Optional stock symbol to filter by
        limit: Maximum number of predictions to return
    
    Returns:
        List of prediction dictionaries
    """
    conn = connect_db()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    
    if symbol:
        cursor.execute(
            """SELECT id, symbol, prediction_date, predicted_movement, confidence, actual_movement
               FROM prediction_history 
               WHERE symbol = %s
               ORDER BY prediction_date DESC
               LIMIT %s""",
            (symbol, limit)
        )
    else:
        cursor.execute(
            """SELECT id, symbol, prediction_date, predicted_movement, confidence, actual_movement
               FROM prediction_history 
               ORDER BY prediction_date DESC
               LIMIT %s""",
            (limit,)
        )
    
    predictions = []
    for row in cursor.fetchall():
        predictions.append({
            "id": row[0],
            "symbol": row[1],
            "date": row[2].strftime("%Y-%m-%d"),
            "predicted_movement": row[3],
            "confidence": row[4],
            "actual_movement": row[5]
        })
    
    conn.close()
    return predictions

def save_portfolio_simulation(
    start_date: datetime,
    end_date: datetime,
    initial_balance: float,
    final_balance: float,
    roi: float,
    trades: List[Dict[str, Any]],
    strategy: str = "ai_prediction"
) -> bool:
    """
    Save a portfolio simulation to the database
    
    Args:
        start_date: Simulation start date
        end_date: Simulation end date
        initial_balance: Initial portfolio balance
        final_balance: Final portfolio balance
        roi: Return on investment percentage
        trades: List of trade dictionaries
        strategy: Strategy name
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = connect_db()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """INSERT INTO portfolio_simulation 
               (start_date, end_date, initial_balance, final_balance, roi, trades, strategy) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (
                start_date,
                end_date,
                initial_balance,
                final_balance,
                roi,
                json.dumps(trades),
                strategy
            )
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving portfolio simulation: {e}")
        conn.close()
        return False

def update_actual_movements() -> int:
    """
    Update actual price movements for predictions
    
    Returns:
        int: Number of predictions updated
    """
    from datetime import timedelta
    from data.stock_data import get_external_stock_data
    
    conn = connect_db()
    if conn is None:
        return 0
    
    cursor = conn.cursor()
    
    # Get predictions that need updating (1+ day old and actual_movement is NULL)
    yesterday = datetime.now() - timedelta(days=1)
    cursor.execute(
        """SELECT id, symbol, prediction_date 
           FROM prediction_history 
           WHERE actual_movement IS NULL AND prediction_date < %s""",
        (yesterday,)
    )
    
    predictions_to_update = cursor.fetchall()
    updated_count = 0
    
    for pred_id, symbol, pred_date in predictions_to_update:
        # Get actual stock data for the day after prediction
        next_day = pred_date + timedelta(days=1)
        
        df = get_external_stock_data(symbol, period="5d")
        if df is None:
            continue
            
        # Find the row for the prediction date and next day
        df['date'] = pd.to_datetime(df['date'])
        pred_row = df[df['date'].dt.date == pred_date.date()]
        next_row = df[df['date'].dt.date == next_day.date()]
        
        if len(pred_row) == 0 or len(next_row) == 0:
            continue
        
        # Determine actual movement
        actual_movement = bool(next_row.iloc[0]['close_price'] > pred_row.iloc[0]['close_price'])
        
        # Update database
        cursor.execute(
            "UPDATE prediction_history SET actual_movement = %s WHERE id = %s",
            (actual_movement, pred_id)
        )
        updated_count += 1
    
    conn.commit()
    conn.close()
    
    return updated_count