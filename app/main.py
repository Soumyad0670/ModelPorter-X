# app/main.py (updated to use models module)
from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flasgger import Swagger
import logging
from datetime import datetime

# Import from local modules
from .auth import api_key_required
from .models import model_manager, validate_model_input, format_prediction_response
from .models.model_utils import get_feature_names, get_class_names
from app.main import app

# Create blueprint
bp = Blueprint('main', __name__)

# Initialize extensions (will be initialized in create_app)
limiter = Limiter()
swagger = Swagger()

@bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - Monitoring
    responses:
      200:
        description: API is healthy
    """
    models_loaded = len(model_manager.loaded_versions) > 0
    status = 'healthy' if models_loaded else 'degraded'
    
    return jsonify({
        'status': status,
        'models_loaded': model_manager.loaded_versions,
        'active_model': model_manager.active_model_version,
        'timestamp': datetime.now().isoformat()
    })

@bp.route('/predict', methods=['POST'])
@api_key_required
@limiter.limit("10 per minute")
def predict():
    """
    Make a prediction using the ML model
    ---
    tags:
      - Predictions
    parameters:
      - in: header
        name: X-API-KEY
        required: true
        schema:
          type: string
        description: API key for authentication
      - in: body
        name: features
        required: true
        schema:
          type: object
          properties:
            features:
              type: array
              items:
                type: number
              example: [5.1, 3.5, 1.4, 0.2]
            model_version:
              type: string
              description: Specific model version to use
              example: v1
    responses:
      200:
        description: Prediction result
      400:
        description: Invalid input
      401:
        description: Unauthorized
      500:
        description: Server error
    """
    try:
        # Log the request
        logging.info(f"Prediction request from {request.remote_addr}")
        
        # Get the data from the request
        data = request.get_json()
        
        if not data or 'features' not in data:
            logging.warning("Missing features in request")
            return jsonify({'error': 'Features array is required'}), 400
        
        # Validate input
        validation_result = validate_model_input(data['features'])
        if not validation_result['valid']:
            logging.warning(f"Invalid features: {validation_result['message']}")
            return jsonify({'error': validation_result['message']}), 400
        
        # Get model version from request or use default
        model_version = data.get('model_version')
        
        # Make prediction
        prediction_result = model_manager.predict(data['features'], model_version)
        
        # Format response
        response_data = format_prediction_response(prediction_result)
        
        # Log successful prediction
        logging.info(f"Prediction successful: {response_data}")
        
        return jsonify(response_data)
        
    except ValueError as e:
        logging.warning(f"Prediction validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/models', methods=['GET'])
@api_key_required
def list_models():
    """
    List all loaded models and their information
    ---
    tags:
      - Models
    responses:
      200:
        description: List of loaded models
    """
    try:
        models_info = model_manager.get_all_models_info()
        return jsonify({
            'models': models_info,
            'active_model': model_manager.active_model_version,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logging.error(f"Error getting models info: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/models/<version>', methods=['GET'])
@api_key_required
def get_model_info(version):
    """
    Get information about a specific model version
    ---
    tags:
      - Models
    parameters:
      - in: path
        name: version
        required: true
        schema:
          type: string
        description: Model version identifier
    responses:
      200:
        description: Model information
      404:
        description: Model not found
    """
    try:
        model_info = model_manager.get_model_info(version)
        if 'error' in model_info:
            return jsonify({'error': model_info['error']}), 404
        
        return jsonify(model_info)
    except Exception as e:
        logging.error(f"Error getting model info for {version}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Error handlers
@bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@bp.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded'}), 429

# Export the blueprint
__all__ = ['bp']