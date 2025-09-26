# __init__.py
"""
ML Model Deployment API

A production-ready Flask application for serving machine learning predictions
with authentication, validation, logging, and containerization.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import key components for easier access
try:
	from .main import app
	from .auth import api_key_required
	from .validation import validate_features
except ImportError:
	# For development, allow partial imports if not all modules are ready
	app = None

# Package metadata
__all__ = ['app', 'api_key_required', 'validate_features', '__version__']