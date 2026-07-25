import os
import uuid
import tempfile
from fastapi import APIRouter, File, UploadFile, HTTPException
from schemas import NpkAnalysisInput
from services.analysis_service import AnalysisService
from config import settings
from inference_sdk import InferenceHTTPClient

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])

@router.post("/bwd")
async def analyze_bwd(file: UploadFile = File(...)):
    """
    Analyze leaf image for BWD (Blade Width Detection) score.
    Accepts an uploaded image file.
    """
    try:
        contents = await file.read()
        result = AnalysisService.analyze_leaf_image(contents)
        if result is None:
            raise HTTPException(status_code=400, detail="No leaf-like area detected (green mask empty)")
        return {
            'success': True,
            **result
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Leaf image analysis failed: {str(e)}")

@router.post("/npk")
def analyze_npk(payload: NpkAnalysisInput):
    """
    Analyze soil NPK values and return recommendations.
    Accepts NPK soil values via JSON.
    """
    try:
        result = AnalysisService.analyze_npk_values(
            payload.n_value,
            payload.p_value,
            payload.k_value
        )
        return {
            'success': True,
            'analysis': result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NPK analysis failed: {str(e)}")

@router.post("/disease-advanced")
async def analyze_disease_advanced(file: UploadFile = File(...)):
    """
    Analyze plant disease using Roboflow AI workflow.
    Accepts an uploaded leaf image file.
    """
    # Check extension
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PNG, JPG, JPEG allowed.")
    
    # Save to a temporary file
    temp_dir = settings.TEMP_IMAGE_FOLDER
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, f"{uuid.uuid4()}.jpg")
    
    try:
        contents = await file.read()
        with open(temp_path, "wb") as f:
            f.write(contents)
            
        # Initialize Roboflow client
        roboflow_api_key = os.environ.get('ROBOFLOW_API_KEY', 'your_roboflow_key_here')
        client = InferenceHTTPClient(
            api_url="https://serverless.roboflow.com",
            api_key=roboflow_api_key
        )
        
        # Run workflow
        result = client.run_workflow(
            workspace_name="andriyanto39",
            workflow_id="detect-and-classify",
            images={"image": temp_path},
            use_cache=True
        )
        
        return {
            'success': True,
            'data': result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Disease analysis failed: {str(e)}")
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
