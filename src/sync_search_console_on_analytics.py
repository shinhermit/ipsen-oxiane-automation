"""
This script creates properties in Google Search Console based on
properties declared in Google Analytics
"""

from src import settings
from src.googleapi.api_connector import get_service


analytics_settings = settings.googleapi["analytics"]
api = get_service(analytics_settings["api_name"])
