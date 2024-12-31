# tests/ml/test_evaluate.py

import os
import pytest
import pandas as pd
from unittest.mock import patch
from joblib import dump
from ml.scripts.evaluate import main as evaluate_main

@pytest.fixture
def mock_evaluate_data(tmp_path):
    """
    Creates a fake test.csv, model_config.json, dataset_config.json,
    and a dummy trained model for evaluation.
    Returns tmp_path for test usage.
    """
    # data/processed/test.csv
    data_dir = tmp_path / "data" / "processed"
    data_dir.mkdir(parents=True)

    test_csv = data_dir / "test.csv"
    df_test = pd.DataFrame({
        "feature1": [5, 6],
        "feature2": [7, 8],
        "feature3": [9, 10],
        "label": [1, 0]
    })
    df_test.to_csv(test_csv, index=False)

    # ml/config
    cfg_dir = tmp_path / "ml" / "config"
    cfg_dir.mkdir(parents=True)

    model_cfg = cfg_dir / "model_config.json"
    model_cfg.write_text("""{
        "save_path": "ml/models/trained_model.joblib"
    }""")

    dataset_cfg = cfg_dir / "dataset_config.json"
    dataset_cfg.write_text(f"""{{
        "test_data_path": "{test_csv}",
        "features": ["feature1", "feature2", "feature3"],
        "target": "label"
    }}""")

    # ml/models + dummy trained model
    model_dir = tmp_path / "ml" / "models"
    model_dir.mkdir(parents=True)
    model_file = model_dir / "trained_model.joblib"

    # Create a trivial RandomForest for testing
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier()
    model.fit([[1,2,3],[2,3,4]], [0,1])  # Minimal training
    dump(model, model_file)

    return tmp_path

@patch("sys.argv", ["evaluate.py"])  # Mock argv
def test_evaluate_script(mock_evaluate_data, monkeypatch, capsys):
    """
    Test that evaluate.py loads the model, reads test data, 
    and prints out "Test Accuracy: ..." and a classification report.
    """
    # 1. Setup
    monkeypatch.chdir(mock_evaluate_data)

    # 2. Exercise
    evaluate_main()

    # 3. Verify
    captured = capsys.readouterr().out

    # Check that the model was loaded
    assert "Model loaded from ml/models/trained_model.joblib" in captured, (
        "Expected message about loading the model was not found."
    )
    # Check for test accuracy
    assert "Test Accuracy:" in captured, (
        "Expected 'Test Accuracy:' in evaluation output."
    )
    # Check for classification report
    assert "Classification Report:" in captured, (
        "Expected 'Classification Report:' in evaluation output."
    )

    print("Test evaluate_script passed.")

@patch("sys.argv", ["evaluate.py"]) 
def test_evaluate_script_with_scaler(mock_evaluate_data, monkeypatch, capsys):
    """
    If the model used a scaler, the script should load 'ml/models/scaler.joblib'
    and apply it to test data. We'll create a dummy scaler joblib for this scenario.
    """
    # 1. Create dummy scaler in ml/models
    scaler_path = mock_evaluate_data / "ml" / "models" / "scaler.joblib"
    from joblib import dump
    from sklearn.preprocessing import StandardScaler
    dummy_scaler = StandardScaler()
    dump(dummy_scaler, scaler_path)

    # 2. Run evaluate
    monkeypatch.chdir(mock_evaluate_data)
    evaluate_main()

    # 3. Verify
    captured = capsys.readouterr().out
    # The script prints "Scaler loaded from ml/models/scaler.joblib" if present
    assert "Scaler loaded from ml/models/scaler.joblib" in captured, (
        "Expected message about loading the scaler was not found."
    )

    print("Test evaluate_script_with_scaler passed.")
