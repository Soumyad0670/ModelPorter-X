# tests/__init__.py
"""
Test package for ML Model Deployment API

This package contains unit and integration tests for the API.
"""

import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import test modules
from .test_api import TestMLAPI

__all__ = ['TestMLAPI']

from flask import Flask
from .main import bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app