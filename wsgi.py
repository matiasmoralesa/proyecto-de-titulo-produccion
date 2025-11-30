"""
WSGI config wrapper for Railway deployment.
This file redirects to the actual WSGI application in backend/config/wsgi.py
"""
import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the actual WSGI application
from config.wsgi import application

__all__ = ['application']
