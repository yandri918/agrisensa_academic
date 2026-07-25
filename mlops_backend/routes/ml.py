from fastapi import APIRouter, HTTPException
from schemas import (
    CropRecommendInput,
    YieldPredictInput,
    YieldPlanInput,
    FertilizerBagsInput,
    SuccessPredictInput
)
from services.ml_service import MLService

router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])

@router.post("/recommend-crop")
def recommend_crop(payload: CropRecommendInput):
    """Recommend crop based on soil and climate data."""
    try:
        data = payload.model_dump()
        result = MLService.recommend_crop(data)
        return {
            'success': True,
            'recommended_crop': result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crop recommendation failed: {str(e)}")

@router.post("/predict-yield")
def predict_yield(payload: YieldPredictInput):
    """Predict crop yield based on input parameters."""
    try:
        data = payload.model_dump()
        prediction = MLService.predict_yield(data)
        return {
            'success': True,
            'predicted_yield_ton_ha': prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yield prediction failed: {str(e)}")

@router.post("/predict-yield-advanced")
def predict_yield_advanced(payload: YieldPredictInput):
    """Predict yield with explainable AI (SHAP values)."""
    try:
        data = payload.model_dump()
        result = MLService.predict_yield_advanced(data)
        return {
            'success': True,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Advanced prediction failed: {str(e)}")

@router.post("/generate-yield-plan")
def generate_yield_plan(payload: YieldPlanInput):
    """Generate plan to achieve target yield."""
    try:
        plan = MLService.generate_yield_plan(
            payload.commodity,
            payload.target_yield
        )
        if not plan:
            raise HTTPException(status_code=404, detail="Could not generate plan for target yield")
        return {
            'success': True,
            'plan': plan
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plan generation failed: {str(e)}")

@router.post("/calculate-fertilizer-bags")
def calculate_fertilizer_bags(payload: FertilizerBagsInput):
    """Calculate fertilizer bags needed for nutrient requirement."""
    try:
        result = MLService.calculate_fertilizer_bags(
            payload.nutrient_needed,
            payload.nutrient_amount_kg,
            payload.fertilizer_type
        )
        if not result:
            raise HTTPException(status_code=400, detail="Calculation failed. Check fertilizer type and nutrient.")
        return {
            'success': True,
            'required_fertilizer_kg': result['required_kg'],
            'fertilizer_name': result['fertilizer_name'],
            'nutrient_needed': result['nutrient_needed'],
            'nutrient_amount_kg': result['nutrient_amount_kg']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@router.post("/predict-success")
def predict_success(payload: SuccessPredictInput):
    """Predict success probability for crop cultivation."""
    try:
        data = payload.model_dump()
        result = MLService.predict_success(data)
        return {
            'success': True,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Success prediction failed: {str(e)}")
