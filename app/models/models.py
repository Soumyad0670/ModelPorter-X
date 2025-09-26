# app/models/models.py
"""
Models module for ML Model Deployment API

This module contains model loading, management, and prediction utilities.
"""

import joblib
import numpy as np
import logging
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class ModelManager:
    """
    Manager class for handling ML models with versioning and fallback support.
    """
    
    def __init__(self, models_dir: str = 'app/models'):
        self.models_dir = models_dir
        self.models: Dict[str, Any] = {}
        self.active_model_version = 'v1'
        self.loaded_versions: List[str] = []
    
    def load_model(self, version: str = 'v1', model_path: Optional[str] = None) -> bool:
        """
        Load a specific model version.
        
        Args:
            version (str): Model version identifier
            model_path (str, optional): Custom path to model file
            
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            if model_path is None:
                model_path = os.path.join(self.models_dir, f'model_{version}.pkl')
            
            if not os.path.exists(model_path):
                logger.error(f"Model file not found: {model_path}")
                return False
            
            model = joblib.load(model_path)
            self.models[version] = model
            self.loaded_versions.append(version)
            logger.info(f"Model version {version} loaded successfully from {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model version {version}: {str(e)}")
            return False
    
    def load_all_models(self) -> Dict[str, bool]:
        """
        Load all available models in the models directory.
        
        Returns:
            Dict[str, bool]: Dictionary with version as key and load status as value
        """
        results = {}
        try:
            # Look for model files in the models directory
            for file_name in os.listdir(self.models_dir):
                if file_name.startswith('model_') and file_name.endswith('.pkl'):
                    version = file_name.replace('model_', '').replace('.pkl', '')
                    results[version] = self.load_model(version)
            
            # If no models found, try loading default
            if not results:
                results['v1'] = self.load_model('v1')
                
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
        
        return results
    
    def predict(self, features: List[float], version: Optional[str] = None) -> Dict[str, Any]:
        """
        Make a prediction using the specified model version.
        
        Args:
            features (List[float]): Input features for prediction
            version (str, optional): Model version to use
            
        Returns:
            Dict[str, Any]: Prediction results with metadata
        """
        if version is None:
            version = self.active_model_version
        
        if version not in self.models:
            error_msg = f"Model version {version} not loaded"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            # Validate input features
            if len(features) != 4:  # Assuming Iris dataset with 4 features
                error_msg = f"Expected 4 features, got {len(features)}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            # Convert to numpy array and reshape
            features_array = np.array(features).reshape(1, -1)
            
            # Make prediction
            model = self.models[version]
            prediction = model.predict(features_array)
            prediction_proba = model.predict_proba(features_array)
            
            # Get class names if available
            class_names = getattr(model, 'classes_', None)
            if class_names is not None:
                class_name = str(class_names[prediction[0]]) if len(class_names) > prediction[0] else 'unknown'
            else:
                class_name = f'class_{prediction[0]}'
            
            result = {
                'prediction': int(prediction[0]),
                'class_name': class_name,
                'confidence': prediction_proba[0].tolist(),
                'confidence_max': float(np.max(prediction_proba[0])),
                'model_version': version,
                'timestamp': datetime.now().isoformat(),
                'features_used': features
            }
            
            logger.info(f"Prediction successful: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Prediction error with model {version}: {str(e)}")
            raise
    
    def get_model_info(self, version: str) -> Dict[str, Any]:
        """
        Get information about a loaded model.
        
        Args:
            version (str): Model version identifier
            
        Returns:
            Dict[str, Any]: Model information
        """
        if version not in self.models:
            return {'error': f'Model version {version} not loaded'}
        
        model = self.models[version]
        info = {
            'version': version,
            'model_type': type(model).__name__,
            'loaded': True,
            'n_features': getattr(model, 'n_features_in_', 'unknown'),
            'n_classes': getattr(model, 'n_classes_', 'unknown') if hasattr(model, 'n_classes_') else 'unknown',
            'classes': getattr(model, 'classes_', []).tolist() if hasattr(model, 'classes_') else []
        }
        
        # Add model-specific attributes
        if hasattr(model, 'estimators_'):
            info['n_estimators'] = len(model.estimators_)
        
        return info
    
    def get_all_models_info(self) -> Dict[str, Any]:
        """
        Get information about all loaded models.
        
        Returns:
            Dict[str, Any]: Information about all models
        """
        return {version: self.get_model_info(version) for version in self.loaded_versions}
    
    def set_active_version(self, version: str) -> bool:
        """
        Set the active model version for predictions.
        
        Args:
            version (str): Model version identifier
            
        Returns:
            bool: True if version was set successfully, False otherwise
        """
        if version in self.models:
            self.active_model_version = version
            logger.info(f"Active model version set to {version}")
            return True
        else:
            logger.warning(f"Cannot set active version: model {version} not loaded")
            return False

# Global model manager instance
model_manager = ModelManager()

def init_models(app=None):
    """
    Initialize models during application startup.
    
    Args:
        app: Flask application instance (optional)
    """
    try:
        # Get models directory from app config or use default
        models_dir = getattr(app, 'config', {}).get('MODELS_DIR', 'app/models') if app else 'app/models'
        
        global model_manager
        model_manager = ModelManager(models_dir)
        
        # Load all available models
        load_results = model_manager.load_all_models()
        
        if not any(load_results.values()):
            logger.warning("No models loaded successfully. Application may not function properly.")
        
        logger.info(f"Models initialization completed. Loaded versions: {model_manager.loaded_versions}")
        return load_results
        
    except Exception as e:
        logger.error(f"Failed to initialize models: {str(e)}")
        return {}