def create_risk_zone(prediction):
    """
    Convert an AI prediction into a GIS-ready risk zone.
    """

    risk_level = prediction["risk_level"]

    zone_mapping = {
        "LOW": {
            "zone": "LOW_RISK_ZONE",
            "color": "green"
        },
        "MEDIUM": {
            "zone": "MEDIUM_RISK_ZONE",
            "color": "yellow"
        },
        "HIGH": {
            "zone": "HIGH_RISK_ZONE",
            "color": "orange"
        },
        "CRITICAL": {
            "zone": "CRITICAL_RISK_ZONE",
            "color": "red"
        }
    }

    zone_info = zone_mapping.get(
        risk_level,
        {
            "zone": "UNKNOWN",
            "color": "gray"
        }
    )

    return {
        "latitude": prediction["latitude"],
        "longitude": prediction["longitude"],
        "risk_score": prediction["risk_score"],
        "risk_level": risk_level,
        "risk_zone": zone_info["zone"],
        "display_color": zone_info["color"],
        "disaster_type": prediction["disaster_type"],
        "confidence": prediction["confidence"]
    }


if __name__ == "__main__":

    sample_prediction = {
        "risk_score": 75,
        "risk_level": "HIGH",
        "confidence": 0.74,
        "disaster_type": "FLOOD",
        "latitude": 18.05,
        "longitude": 79.67
    }

    zone = create_risk_zone(sample_prediction)

    print("Risk Zone")
    print("---------")
    print(f"Zone          : {zone['risk_zone']}")
    print(f"Risk Level    : {zone['risk_level']}")
    print(f"Risk Score    : {zone['risk_score']}")
    print(f"Display Color : {zone['display_color']}")
    print(f"Latitude      : {zone['latitude']}")
    print(f"Longitude     : {zone['longitude']}")