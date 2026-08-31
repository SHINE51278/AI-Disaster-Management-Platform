from fastapi import FastAPI
from pydantic import BaseModel, Field

from .predict import predict_risk
from .risk_zone import create_risk_zone
from .geojson import prediction_to_feature


app = FastAPI(
    title="AI Disaster Risk Prediction API",
    version="1.0.0"
)


class RiskRequest(BaseModel):
    rainfall: float = Field(..., ge=0)
    river_level: float = Field(..., ge=0)
    temperature: float
    humidity: float = Field(..., ge=0, le=100)
    latitude: float
    longitude: float


@app.get("/")
def home():
    return {
        "message": "AI Risk Prediction API is running"
    }


@app.post("/api/v1/ai/risk/predict")
def predict(request: RiskRequest):

    prediction = predict_risk(
        rainfall=request.rainfall,
        river_level=request.river_level,
        temperature=request.temperature,
        humidity=request.humidity,
        latitude=request.latitude,
        longitude=request.longitude
    )

    risk_zone = create_risk_zone(prediction)

    feature = prediction_to_feature(risk_zone)

    return {
        **risk_zone,
        "geojson": feature
    }