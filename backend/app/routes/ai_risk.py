from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from backend.app.core.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.services.risk_ai import predict_risk


router = APIRouter(
    prefix="/ai/risk",
    tags=["AI Risk Prediction"],
)


class RiskPredictionRequest(BaseModel):
    rainfall: float = Field(..., ge=0)
    river_level: float = Field(..., ge=0)
    temperature: float
    humidity: float = Field(..., ge=0, le=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


@router.post("/predict")
def risk_prediction(
    request: RiskPredictionRequest,
    current_user: User = Depends(get_current_user),
):
    return predict_risk(
        rainfall=request.rainfall,
        river_level=request.river_level,
        temperature=request.temperature,
        humidity=request.humidity,
        latitude=request.latitude,
        longitude=request.longitude,
    )