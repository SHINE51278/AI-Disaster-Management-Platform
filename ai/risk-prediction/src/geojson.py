import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_PATH = OUTPUT_DIR / "risk_zones.geojson"


def prediction_to_feature(prediction):
    """Convert one risk prediction into a GeoJSON feature."""

    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                prediction["longitude"],
                prediction["latitude"]
            ]
        },
        "properties": {
            "risk_score": prediction["risk_score"],
            "risk_level": prediction["risk_level"],
            "risk_zone": prediction["risk_zone"],
            "display_color": prediction["display_color"],
            "disaster_type": prediction["disaster_type"],
            "confidence": prediction["confidence"]
        }
    }


def save_geojson(predictions):
    """Save risk predictions as a GeoJSON FeatureCollection."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    features = [
        prediction_to_feature(prediction)
        for prediction in predictions
    ]

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(geojson, file, indent=2)

    print(f"GeoJSON saved to: {OUTPUT_PATH}")


if __name__ == "__main__":

    sample_predictions = [
        {
            "latitude": 17.98,
            "longitude": 79.60,
            "risk_score": 25,
            "risk_level": "LOW",
            "risk_zone": "LOW_RISK_ZONE",
            "display_color": "green",
            "disaster_type": "FLOOD",
            "confidence": 0.90
        },
        {
            "latitude": 18.02,
            "longitude": 79.64,
            "risk_score": 50,
            "risk_level": "MEDIUM",
            "risk_zone": "MEDIUM_RISK_ZONE",
            "display_color": "yellow",
            "disaster_type": "FLOOD",
            "confidence": 0.82
        },
        {
            "latitude": 18.05,
            "longitude": 79.67,
            "risk_score": 75,
            "risk_level": "HIGH",
            "risk_zone": "HIGH_RISK_ZONE",
            "display_color": "orange",
            "disaster_type": "FLOOD",
            "confidence": 0.74
        },
        {
            "latitude": 18.08,
            "longitude": 79.70,
            "risk_score": 95,
            "risk_level": "CRITICAL",
            "risk_zone": "CRITICAL_RISK_ZONE",
            "display_color": "red",
            "disaster_type": "FLOOD",
            "confidence": 0.91
        }
    ]

    save_geojson(sample_predictions)