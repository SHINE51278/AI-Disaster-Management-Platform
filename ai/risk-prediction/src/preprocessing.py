import pandas as pd
from pathlib import Path


# Get the project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset location
DATA_PATH = BASE_DIR / "data" / "raw" / "flood_risk_data.csv"


def load_data():
    """Load the flood risk dataset."""
    df = pd.read_csv(DATA_PATH)
    return df


def preprocess_data(df):
    """Prepare data for model training."""

    # Remove rows containing missing values
    df = df.dropna()

    # Features used by the model
    features = [
        "rainfall",
        "river_level",
        "temperature",
        "humidity",
        "latitude",
        "longitude",
    ]

    # Target variable
    target = "risk_level"

    X = df[features]
    y = df[target]

    return X, y


if __name__ == "__main__":
    df = load_data()

    X, y = preprocess_data(df)

    print("Dataset loaded successfully!")
    print(f"Total records: {len(df)}")
    print(f"Features: {list(X.columns)}")
    print(f"Risk classes: {list(y.unique())}")