import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

class Config:
    """Configuration class for the FastAPI MLOps API."""
    
    # Base directory of the project
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # ML Models path (default to the subfolder in project)
    ML_MODELS_PATH = os.getenv('ML_MODELS_PATH', os.path.join(BASE_DIR, 'ml_models'))
    
    # Paths of individual pickled models
    MODEL_PATHS = {
        'bwd': 'bwd_model.pkl',
        'recommendation': 'recommendation_model.pkl',
        'crop_recommendation': 'crop_recommendation_model.pkl',
        'yield_prediction': 'yield_prediction_model.pkl',
        'advanced_yield': 'advanced_yield_model.pkl',
        'shap_explainer': 'shap_explainer.pkl',
        'success': 'success_model.pkl'
    }
    
    # Temporary folders
    TEMP_IMAGE_FOLDER = os.getenv('TEMP_IMAGE_FOLDER', os.path.join(BASE_DIR, 'uploads', 'temp_images'))
    
    # API & Port Configuration
    PORT = int(os.getenv('PORT', 8000))
    
    # Cors configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Singleton instance
settings = Config()
