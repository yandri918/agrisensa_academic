from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class CropRecommendInput(BaseModel):
    n_value: float = Field(..., description="Nitrogen value in soil", example=90.0)
    p_value: float = Field(..., description="Phosphorus value in soil", example=42.0)
    k_value: float = Field(..., description="Potassium value in soil", example=43.0)
    temperature: float = Field(..., description="Temperature in °C", example=20.8)
    humidity: float = Field(..., description="Humidity percentage", example=82.0)
    ph: float = Field(..., description="Soil pH level", example=6.5)
    rainfall: float = Field(..., description="Rainfall in mm", example=202.9)

class YieldPredictInput(BaseModel):
    nitrogen: float = Field(..., description="Nitrogen value (kg/ha)", example=120.0)
    phosphorus: float = Field(..., description="Phosphorus value (kg/ha)", example=75.0)
    potassium: float = Field(..., description="Potassium value (kg/ha)", example=75.0)
    temperature: float = Field(..., description="Temperature in °C", example=26.5)
    rainfall: float = Field(..., description="Rainfall in mm", example=1800.0)
    ph: float = Field(..., description="Soil pH level", example=6.2)

class YieldPlanInput(BaseModel):
    commodity: str = Field(..., description="Commodity name (e.g. padi, cabai, jagung)", example="padi")
    target_yield: float = Field(..., description="Target yield in ton/ha", example=6.5)

class FertilizerBagsInput(BaseModel):
    nutrient_needed: str = Field(..., description="Nutrient needed ('N', 'P', 'K')", example="N")
    nutrient_amount_kg: float = Field(..., description="Nutrient amount needed in kg", example=45.0)
    fertilizer_type: str = Field(..., description="Fertilizer product identifier ('urea', 'sp36', 'kcl', etc.)", example="urea")

class SuccessPredictInput(BaseModel):
    nitrogen: float = Field(..., description="Nitrogen value (kg/ha)", example=120.0)
    phosphorus: float = Field(..., description="Phosphorus value (kg/ha)", example=75.0)
    potassium: float = Field(..., description="Potassium value (kg/ha)", example=75.0)
    temperature: float = Field(..., description="Temperature in °C", example=26.5)
    rainfall: float = Field(..., description="Rainfall in mm", example=1800.0)
    ph: float = Field(..., description="Soil pH level", example=6.2)

class NpkAnalysisInput(BaseModel):
    n_value: float = Field(..., description="Nitrogen value in soil", example=150.0)
    p_value: float = Field(..., description="Phosphorus value in soil", example=25.0)
    k_value: float = Field(..., description="Potassium value in soil", example=180.0)
