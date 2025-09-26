# app/validation.py
import numpy as np

def validate_features(features):
    """
    Validate the features array
    """
    if not isinstance(features, list):
        return {'valid': False, 'message': 'Features must be an array'}
    
    if len(features) != 4:
        return {'valid': False, 'message': 'Features array must contain exactly 4 values'}
    
    for i, value in enumerate(features):
        try:
            float_value = float(value)
            if not (0 <= float_value <= 10):  # Reasonable range for iris features
                return {'valid': False, 'message': f'Feature at index {i} must be between 0 and 10'}
        except (ValueError, TypeError):
            return {'valid': False, 'message': f'Feature at index {i} must be a number'}
    
    return {'valid': True, 'message': 'Features are valid'}