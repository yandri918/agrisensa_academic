import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes import ml, analysis

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger("mlops_api")

# Initialize FastAPI App
app = FastAPI(
    title="AgriSensa MLOps API",
    description="Unified Machine Learning and Image Analysis API for precision agriculture.",
    version="1.0.0"
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(ml.router)
app.include_router(analysis.router)

@app.on_event("startup")
def startup_event():
    """Execute code on startup."""
    # Ensure temporary upload directory exists
    os.makedirs(settings.TEMP_IMAGE_FOLDER, exist_ok=True)
    logger.info("Temporary folders initialized")
    
    # Warm up models
    logger.info("Warming up machine learning models...")
    from ml_models.model_loader import ModelLoader
    ModelLoader.get_model('crop_recommendation')
    ModelLoader.get_model('yield_prediction')
    logger.info("Startup complete. API is ready.")

@app.get("/")
def read_root():
    """API Info root endpoint."""
    return {
        "name": "AgriSensa MLOps API",
        "version": "1.0.0",
        "description": "Production MLOps inference engine for AgriSensa.",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    # Simple check for model directory existence
    models_ready = os.path.exists(settings.ML_MODELS_PATH)
    return {
        "status": "healthy" if models_ready else "degraded",
        "models_dir": settings.ML_MODELS_PATH,
        "models_present": models_ready
    }
