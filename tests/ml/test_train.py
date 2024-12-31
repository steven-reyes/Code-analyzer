# tests/ml/test_train.py

import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from ml.scripts.train import main as train_main

@pytest.fixture
def mock_data(tmp_path):
    """
    Creates a fake dataset (train.csv) and config files (model_config.json, dataset_config.json)
    under a temporary path, returning tmp_path for use by tests.
    
    By default, we'll NOT specify a scaler. If you want to test the scaler,
    you can modify model_config to include:
        "scaler": {"type": "StandardScaler"}
    """
    data_dir = tmp_path / "data" / "processed"
    data_dir.mkdir(parents=True)

    # Create a small training dataset
    train_csv = data_dir / "train.csv"
    df = pd.DataFrame({
        "feature1": [1, 2, 3, 4, 5],
        "feature2": [2, 4, 6, 8, 10],
        "feature3": [10, 9, 8, 7, 6],
        "label": [0, 1, 0, 1, 0]
    })
    df.to_csv(train_csv, index=False)

    # Create config directories
    config_dir = tmp_path / "ml" / "config"
    config_dir.mkdir(parents=True)
    
    # Model config (no scaler by default)
    model_cfg = config_dir / "model_config.json"
    model_cfg.write_text("""{
        "model_type": "RandomForestClassifier",
        "hyperparameters": {
            "n_estimators": 10,
            "random_state": 42
        },
        "save_path": "ml/models/trained_model.joblib"
    }""")

    # Dataset config
    dataset_cfg = config_dir / "dataset_config.json"
    dataset_cfg.write_text(f"""{{
        "train_data_path": "{train_csv}",
        "features": ["feature1", "feature2", "feature3"],
        "target": "label"
    }}""")

    return tmp_path

@patch("sys.argv", ["train.py"])  # Mock argv so train_main() doesn't parse real CLI args
def test_train_script(mock_data, monkeypatch, capsys):
    """
    Test that train.py can run end-to-end, saving a model and printing:
      - "Training complete."
      - "Validation Score: ..."
      - "Model saved to ..."
    """
    # 1. Setup: change working directory to our temporary directory
    monkeypatch.chdir(mock_data)

    # Ensure ml/models folder doesn't exist yet
    model_dir = mock_data / "ml" / "models"
    assert not model_dir.exists(), "ml/models directory should not exist before training."

    # 2. Exercise: run the train_main() function
    train_main()

    # 3. Verify:
    #    a) Check that ml/models directory and .joblib file exist
    assert model_dir.exists(), "Training script did not create ml/models directory."
    joblib_files = list(model_dir.glob("*.joblib"))
    assert len(joblib_files) > 0, "No .joblib model was saved after training."

    #    b) Capture stdout and confirm expected messages
    captured = capsys.readouterr().out
    assert "Training complete." in captured, "Expected 'Training complete.' message not found."
    assert "Validation Score:" in captured, "Expected 'Validation Score:' message not found."
    assert "Model saved to ml/models/trained_model.joblib" in captured, (
        "Expected 'Model saved to ml/models/trained_model.joblib' not found."
    )

    #    c) If no scaler specified, confirm no mention of scaler saving
    assert "scaler saved" not in captured, "Scaler mention found even though no scaler config was specified."

    print("Test train_script passed.")


@patch("sys.argv", ["train.py"]) 
def test_train_script_with_scaler(mock_data, monkeypatch, capsys):
    """
    Same as above, but we'll update the model config to include a scaler.
    This ensures the script saves a scaler.joblib and prints relevant messages.
    """
    # 1. Update the model_config.json to include a StandardScaler
    model_config_path = mock_data / "ml" / "config" / "model_config.json"
    model_config_path.write_text("""{
        "model_type": "RandomForestClassifier",
        "hyperparameters": {
            "n_estimators": 10,
            "random_state": 42
        },
        "scaler": {
            "type": "StandardScaler"
        },
        "save_path": "ml/models/trained_model.joblib"
    }""")

    # 2. Change dir & run
    monkeypatch.chdir(mock_data)
    train_main()

    # 3. Assertions
    model_dir = mock_data / "ml" / "models"
    assert model_dir.exists()
    joblib_files = list(model_dir.glob("*.joblib"))
    assert len(joblib_files) >= 2, (
        "Expected both a model and a scaler .joblib file (2+) when using StandardScaler."
    )

    captured = capsys.readouterr().out
    assert "scaler saved to ml/models/scaler.joblib" in captured, (
        "Expected mention of scaler saving but did not find it."
    )

    print("Test train_script_with_scaler passed.")
