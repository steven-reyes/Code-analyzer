# ml/scripts/train.py

import json
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from joblib import dump

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
    The main training script. 
    1. Loads model_config.json and dataset_config.json
    2. Reads train_data from CSV
    3. Optionally splits data into train/val
    4. Scales features if specified
    5. Trains a model (RandomForest by default)
    6. Evaluates on validation set
    7. Saves model + optional scaler
    """
    # Load configs
    model_config = load_json_config("ml/config/model_config.json")
    dataset_config = load_json_config("ml/config/dataset_config.json")

    # Read dataset
    train_data = pd.read_csv(dataset_config["train_data_path"])
    features = dataset_config["features"]
    target = dataset_config["target"]

    X = train_data[features]
    y = train_data[target]

    # Optional train/validation split
    X_train, X_val, y_train, y_val = train_test_split(X, y, 
                                                      test_size=0.2, 
                                                      random_state=42)

    # Optional scaler
    scaler = None
    scaler_config = model_config.get("scaler", {})
    if scaler_config.get("type") == "StandardScaler":
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_val = scaler.transform(X_val)

    # Initialize model
    model_type = model_config["model_type"]
    hyperparams = model_config.get("hyperparameters", {})

    if model_type == "RandomForestClassifier":
        model = RandomForestClassifier(**hyperparams)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    # Train
    model.fit(X_train, y_train)
    print("Training complete.")

    # Evaluate on validation set
    val_score = model.score(X_val, y_val)
    print(f"Validation Score: {val_score:.4f}")

    # Save model
    save_path = model_config["save_path"]
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # If we used a scaler, save it separately
    if scaler:
        dump(model, save_path)
        dump(scaler, "ml/models/scaler.joblib")
        print(f"Model saved to {save_path}, scaler saved to ml/models/scaler.joblib")
    else:
        dump(model, save_path)
        print(f"Model saved to {save_path}")


if __name__ == "__main__":
    main()
