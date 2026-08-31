import sys
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

# Allow importing preprocessing.py
sys.path.append(str(Path(__file__).resolve().parent))

from preprocessing import load_data, preprocess_data


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "risk_model.pkl"


def train_model():
    # Load and preprocess data
    df = load_data()
    X, y = preprocess_data(df)

    print("Dataset loaded successfully!")
    print(f"Total records: {len(df)}")
    print(f"Features: {list(X.columns)}")
    print(f"Risk classes: {sorted(y.unique())}")

    # ---------------------------------------------------------
    # 1. Hold-out evaluation
    # ---------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print("\n----------------------------------------")
    print("Hold-out Model Evaluation")
    print("----------------------------------------")
    print(f"Test Accuracy: {accuracy:.2f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0
        )
    )

    # ---------------------------------------------------------
    # 2. Stratified cross-validation
    # ---------------------------------------------------------
    class_counts = y.value_counts()

    # Number of folds cannot exceed the number of samples
    # available in the smallest class.
    n_splits = min(5, class_counts.min())

    if n_splits >= 2:
        cv = StratifiedKFold(
            n_splits=n_splits,
            shuffle=True,
            random_state=42
        )

        cv_scores = cross_val_score(
            model,
            X,
            y,
            cv=cv,
            scoring="accuracy"
        )

        print("----------------------------------------")
        print("Cross-Validation Evaluation")
        print("----------------------------------------")
        print(
            f"{n_splits}-Fold CV Accuracy: "
            f"{cv_scores.mean():.2f} ± {cv_scores.std():.2f}"
        )

        print("Fold scores:", [round(score, 2) for score in cv_scores])
    else:
        print("\nCross-validation skipped.")
        print("Reason: insufficient samples per risk class.")

    # ---------------------------------------------------------
    # 3. Train final model using complete dataset
    # ---------------------------------------------------------
    final_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    final_model.fit(X, y)

    # ---------------------------------------------------------
    # 4. Save final model
    # ---------------------------------------------------------
    MODEL_DIR.mkdir(exist_ok=True)

    joblib.dump(final_model, MODEL_PATH)

    print("\n----------------------------------------")
    print("Final Model")
    print("----------------------------------------")
    print("Final model trained using complete dataset.")
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()