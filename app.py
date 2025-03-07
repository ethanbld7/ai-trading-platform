# app.py
"""
Main FastAPI application entry point
"""
import os
import threading
import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api import router
from api.prediction import global_models
from api.stock import get_stock_data
from api.portfolio import simulate
from api.prediction import predict_stock, get_recent, get_history, update_movements

from data.database import create_tables
from data.stock_data import fetch_stock_data
from ml.training import train_model

from api.stock import router as stock_router
from api.prediction import router as prediction_router
from api.portfolio import router as portfolio_router

global_models = {}

app = FastAPI(title="AI-Powered Hedge Fund Analytics")

# Create directories if they don't exist
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Include the router
app.include_router(stock_router)
app.include_router(prediction_router)
app.include_router(portfolio_router)

from config import (
    AVAILABLE_SYMBOLS, INITIAL_SYMBOLS, MODEL_UPDATE_INTERVAL, 
    API_HOST, API_PORT
)

# Create the FastAPI app

# Configure static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include API routes
app.include_router(router)

# Page routes
@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    """
    Main dashboard page
    """
    return templates.TemplateResponse("index.html", {
        "request": request,
        "symbols": AVAILABLE_SYMBOLS
    })

@app.get("/portfolio", response_class=HTMLResponse)
async def get_portfolio(request: Request):
    """
    Portfolio simulator page
    """
    return templates.TemplateResponse("portfolio.html", {
        "request": request,
        "symbols": AVAILABLE_SYMBOLS
    })

@app.get("/predictions", response_class=HTMLResponse)
async def get_predictions_page(request: Request):
    """
    Predictions history page
    """
    return templates.TemplateResponse("predictions.html", {
        "request": request,
        "symbols": AVAILABLE_SYMBOLS
    })

@app.get("/api-docs", response_class=HTMLResponse)
async def get_api_docs(request: Request):
    """
    API documentation page
    """
    return templates.TemplateResponse("api-docs.html", {
        "request": request
    })

# Function to update models periodically
def update_models_task():
    """
    Background task that periodically updates the models
    """
    while True:
        for symbol in AVAILABLE_SYMBOLS:
            fetch_stock_data(symbol)
            global_models[symbol] = train_model(symbol)
        
        # Sleep for the configured interval
        time.sleep(MODEL_UPDATE_INTERVAL)

@app.on_event("startup")
def startup_event():
    """
    Startup event handler that initializes the database and models
    """
    try:
        # Create directories
        os.makedirs("templates", exist_ok=True)
        os.makedirs("static/css", exist_ok=True)
        os.makedirs("static/js", exist_ok=True)
        
        # Create template and static files
        print("Creating template and static files...")
        from utils.file_generator import create_template_files, create_static_files
        create_template_files()
        create_static_files()
        
        # Verify template file was created
        if os.path.exists("templates/index.html"):
            print("Template file created successfully: templates/index.html")
        else:
            print("ERROR: Template file was not created: templates/index.html")
        
        # Create database tables
        if create_tables():
            # Fetch data and train models for initial symbols
            for symbol in INITIAL_SYMBOLS:
                print(f"Initializing data and model for {symbol}...")
                try:
                    fetch_stock_data(symbol)
                    global_models[symbol] = train_model(symbol)
                except Exception as e:
                    print(f"Error initializing {symbol}: {e}")
                    continue
        
        # Start background task for model updates
        thread = threading.Thread(target=update_models_task, daemon=True)
        thread.start()
    except Exception as e:
        print(f"Error during startup: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)