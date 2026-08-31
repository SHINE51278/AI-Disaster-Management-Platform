from pathlib import Path

import joblib
import pandas as pd


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Trained model
MODEL_PATH = BASE_DIR / "models" / "risk_model.pkl"


# Load the trained model
model = joblib.load(MODEL_PATH)


def predict_risk(
    rainfall,
    river_level,
    temperature,
    humidity,
    latitude,
    longitude
):
    """Predict flood risk for a given location."""

    input_data = pd.DataFrame([
        {
            "rainfall": rainfall,
            "river_level": river_level,
            "temperature": temperature,
            "humidity": humidity,
            "latitude": latitude,
            "longitude": longitude,
        }
    ])

    # Predict risk class
    risk_level = model.predict(input_data)[0]

    # Get prediction probabilities
    probabilities = model.predict_proba(input_data)[0]

    # Highest class probability becomes confidence
    confidence = max(probabilities)

    # Convert risk level into a numerical score
    risk_scores = {
        "LOW": 25,
        "MEDIUM": 50,
        "HIGH": 75,
        "CRITICAL": 95,
    }

    # Risk zone and display color
    risk_zones = {
        "LOW": "LOW_RISK_ZONE",
        "MEDIUM": "MEDIUM_RISK_ZONE",
        "HIGH": "HIGH_RISK_ZONE",
        "CRITICAL": "CRITICAL_RISK_ZONE",
    }

    display_colors = {
        "LOW": "green",
        "MEDIUM": "yellow",
        "HIGH": "orange",
        "CRITICAL": "red",
    }

    risk_score = risk_scores.get(risk_level, 0)
    risk_zone = risk_zones.get(risk_level, "UNKNOWN_RISK_ZONE")
    display_color = display_colors.get(risk_level, "gray")

    return {
        "latitude": latitude,
        "longitude": longitude,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_zone": risk_zone,
        "display_color": display_color,
        "disaster_type": "FLOOD",
        "confidence": round(float(confidence), 3),
    }


if __name__ == "__main__":

    result = predict_risk(
        rainfall=150,
        river_level=5.5,
        temperature=24,
        humidity=90,
        latitude=18.05,
        longitude=79.67
    )

    print("Risk Prediction")
    print("----------------")
    print(f"Disaster Type : {result['disaster_type']}")
    print(f"Risk Score    : {result['risk_score']}")
    print(f"Risk Level    : {result['risk_level']}")
    print(f"Risk Zone     : {result['risk_zone']}")
    print(f"Display Color : {result['display_color']}")
    print(f"Confidence    : {result['confidence']}")
    print(f"Latitude      : {result['latitude']}")
    print(f"Longitude     : {result['longitude']}")