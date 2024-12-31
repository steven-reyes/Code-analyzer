# ml/scripts/inference.py

import json
import os
import pandas as pd
from joblib import load

def load_json_config(path: str) -> dict:
    """
    Loads a JSON config file from path.
    Raises FileNotFoundError if file doesn't exist.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    """
    Run inference/predictions on new data using the trained model.
    1. Loads model_config to find model_path
    2. Loads dataset_config for features
    3. Reads new_data.csv
    4. Applies optional scaler
    5. Predicts and prints results
    """
    model_config = load_json_config("ml/config/model_config.json")
    model_path = model_config["save_path"]

    # Load model
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"No model found at {model_path}")
    model = load(model_path)
    print(f"Model loaded from {model_path}")

    # Check for scaler
    scaler_path = "ml/models/scaler.joblib"
    scaler = None
    if os.path.isfile(scaler_path):
        scaler = load(scaler_path)
        print(f"Scaler loaded from {scaler_path}")

    # Load new data
    new_data_path = "data/processed/new_data.csv"
    if not os.path.isfile(new_data_path):
        print(f"No inference data found at {new_data_path}")
        return
    new_data = pd.read_csv(new_data_path)

    # Get features from dataset_config
    dataset_config = load_json_config("ml/config/dataset_config.json")
    features = dataset_config["features"]

    if not all(feature in new_data.columns for feature in features):
        missing_cols = [f for f in features if f not in new_data.columns]
        print(f"Error: missing columns in new_data: {missing_cols}")
        return

    X_new = new_data[features]

    # Scale if needed
    if scaler:
        X_new = scaler.transform(X_new)

    # Predict
    predictions = model.predict(X_new)
    print("Inference Results:")
    for idx, pred in enumerate(predictions):
        print(f"Row {idx}: {pred}")

if __name__ == "__main__":
    main()
