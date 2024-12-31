# ml/scripts/evaluate.py

import json
import os
import pandas as pd
from joblib import load
from sklearn.metrics import accuracy_score, classification_report

def load_json_config(path: str) -> dict:
    """
    Loads a JSON config from the given path.
    Raises FileNotFoundError if file doesn't exist.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    """
    Evaluate the previously trained model on the test dataset.
    1. Loads model_config and dataset_config
    2. Loads model and optional scaler
    3. Reads test_data from CSV
    4. Applies scaler (if any)
    5. Predicts and prints accuracy + classification report
    """
    # Load configs
    model_config = load_json_config("ml/config/model_config.json")
    dataset_config = load_json_config("ml/config/dataset_config.json")

    model_path = model_config["save_path"]
    test_data_path = dataset_config["test_data_path"]
    features = dataset_config["features"]
    target = dataset_config["target"]

    # Load model
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Trained model not found at {model_path}")
    model = load(model_path)
    print(f"Model loaded from {model_path}")

    # Load scaler if present
    scaler_path = "ml/models/scaler.joblib"
    scaler = None
    if os.path.isfile(scaler_path):
        scaler = load(scaler_path)
        print(f"Scaler loaded from {scaler_path}")

    # Load test data
    if not os.path.isfile(test_data_path):
        raise FileNotFoundError(f"Test data not found at {test_data_path}")
    test_data = pd.read_csv(test_data_path)

    X_test = test_data[features]
    y_test = test_data[target]

    # Apply scaler if it exists
    if scaler:
        X_test = scaler.transform(X_test)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc:.4f}\n")

    report = classification_report(y_test, y_pred)
    print("Classification Report:")
    print(report)


if __name__ == "__main__":
    main()
