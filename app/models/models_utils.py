# app/models/model_utils.py
"""
Model utilities for ML Model Deployment API

Utility functions for model management, validation, and operations.
"""

import numpy as np
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

def validate_model_input(features: List[float], expected_length: int = 4) -> Dict[str, Any]:
    """
    Validate input features for model prediction.
    
    Args:
        features (List[float]): Input features to validate
        expected_length (int): Expected number of features
        
    Returns:
        Dict[str, Any]: Validation result with status and message
    """
    if not isinstance(features, list):
        return {'valid': False, 'message': 'Features must be a list'}
    
    if len(features) != expected_length:
        return {
            'valid': False, 
            'message': f'Features array must contain exactly {expected_length} values, got {len(features)}'
        }
    
    for i, value in enumerate(features):
        try:
            float_value = float(value)
            # Reasonable range validation for iris features
            if not (0 <= float_value <= 10):
                return {
                    'valid': False, 
                    'message': f'Feature at index {i} must be between 0 and 10, got {float_value}'
                }
        except (ValueError, TypeError):
            return {
                'valid': False, 
                'message': f'Feature at index {i} must be a number, got {type(value).__name__}'
            }
    
    return {'valid': True, 'message': 'Features are valid'}

def format_prediction_response(prediction_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format prediction response for API output.
    
    Args:
        prediction_result (Dict[str, Any]): Raw prediction result
        
    Returns:
        Dict[str, Any]: Formatted API response
    """
    return {
        'prediction': prediction_result['prediction'],
        'class_name': prediction_result.get('class_name', f'class_{prediction_result["prediction"]}'),
        'confidence': prediction_result['confidence'],
        'confidence_max': prediction_result['confidence_max'],
        'model_version': prediction_result['model_version'],
        'timestamp': prediction_result['timestamp']
    }

def get_feature_names(dataset: str = 'iris') -> List[str]:
    """
    Get feature names for a dataset.
    
    Args:
        dataset (str): Dataset identifier
        
    Returns:
        List[str]: List of feature names
    """
    feature_map = {
        'iris': ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
        'default': ['feature_0', 'feature_1', 'feature_2', 'feature_3']
    }
    
    return feature_map.get(dataset, feature_map['default'])

def get_class_names(dataset: str = 'iris') -> Dict[int, str]:
    """
    Get class names mapping for a dataset.
    
    Args:
        dataset (str): Dataset identifier
        
    Returns:
        Dict[int, str]: Mapping of class indices to names
    """
    class_map = {
        'iris': {
            0: 'Iris-setosa',
            1: 'Iris-versicolor', 
            2: 'Iris-virginica'
        },
        'default': {
            0: 'class_0',
            1: 'class_1',
            2: 'class_2'
        }
    }
    
    return class_map.get(dataset, class_map['default'])