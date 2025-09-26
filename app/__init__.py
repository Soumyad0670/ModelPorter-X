# app/__init__.py (updated with model initialization)
import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app(test_config=None):
    """Application factory function"""
    app = Flask(__name__)
    
    # Configure app
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-key'),
            API_KEY=os.getenv('API_KEY', 'default-api-key'),
            MODELS_DIR=os.getenv('MODELS_DIR', 'app/models'),
            SWAGGER={
                'title': 'ML Model API',
                'uiversion': 3,
                'specs_route': '/docs/'
            }
        )
    else:
        app.config.from_mapping(test_config)
    
    # Initialize logging
    from .logging_config import setup_logging
    setup_logging(app)
    
    # Initialize models
    from .models import init_models
    init_models(app)
    
    # Initialize extensions
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    from flasgger import Swagger
    
    # Create global limiter instance
    app.limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
    )
    
    # Create global swagger instance
    app.swagger = Swagger(app)
    
    # Register blueprints
    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Initialize limiter with app context
    with app.app_context():
        from .main import limiter as bp_limiter
        bp_limiter.init_app(app)
    
    return app