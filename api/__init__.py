# api/__init__.py
"""
API package initialization
"""
from fastapi import APIRouter

from api import stock
from api import prediction
from api import portfolio

# Create a router to include in the main app
router = APIRouter()

# Include routes from modules
# Note: Some routes are defined directly in the modules with their own paths
# due to the original structure, but ideally they would be defined with
# the router.include_router pattern below
router.include_router(stock.router)