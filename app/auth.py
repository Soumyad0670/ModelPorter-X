# app/auth.py
from functools import wraps
from flask import request, jsonify
import os
import logging

logger = logging.getLogger(__name__)

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        valid_api_key = os.getenv('API_KEY', 'default-secret-key')
        
        if not api_key or api_key != valid_api_key:
            logger.warning(f"Invalid API key attempt from {request.remote_addr}")
            return jsonify({'error': 'Invalid or missing API key'}), 401
        
        return f(*args, **kwargs)
    return decorated_function