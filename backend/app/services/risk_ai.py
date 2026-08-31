import httpx

from backend.app.database.database import settings


def predict_risk(
    rainfall: float,
    river_level: float,
    temperature: float,
    humidity: float,
    latitude: float,
    longitude: float,
):
    payload = {
        "rainfall": rainfall,
        "river_level": river_level,
        "temperature": temperature,
        "humidity": humidity,
        "latitude": latitude,
        "longitude": longitude,
    }

    response = httpx.post(
        f"{settings.RISK_AI_URL}/api/v1/ai/risk/predict",
        json=payload,
        timeout=10.0,
    )

    response.raise_for_status()

    return response.json()