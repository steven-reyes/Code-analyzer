# tests/ml/test_inference.py

import os
import pytest
import pandas as pd
from unittest.mock import patch
from joblib import dump
from ml.scripts.inference import main as inference_main

@pytest.fixture
def mock_inference_data(tmp_path):
    """
    Creates a fake new_data.csv, model_config.json, dataset_config.json,
    and a dummy trained model for testing the inference script.
    Returns tmp_path for test usage.
    """
    # data/processed/new_data.csv
    data_dir = tmp_path / "data" / "processed"
    data_dir.mkdir(parents=True)

    new_csv = data_dir / "new_data.csv"
    df_new = pd.DataFrame({
        "feature1": [10, 11],
        "feature2": [12, 13],
        "feature3": [14, 15]
    })
    df_new.to_csv(new_csv, index=False)

    # ml/config
    cfg_dir = tmp_path / "ml" / "config"
    cfg_dir.mkdir(parents=True)

    model_cfg = cfg_dir / "model_config.json"
    model_cfg.write_text("""{
        "save_path": "ml/models/trained_model.joblib"
    }""")

    dataset_cfg = cfg_dir / "dataset_config.json"
    dataset_cfg.write_text(f"""{{
        "features": ["feature1", "feature2", "feature3"]
    }}""")

    # ml/models/trained_model.joblib
    model_dir = tmp_path / "ml" / "models"
    model_dir.mkdir(parents=True)
    model_file = model_dir / "trained_model.joblib"

    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier()
    # Minimal training for a 2-class scenario
    model.fit([[1,2,3],[4,5,6]], [0,1]) 
    dump(model, model_file)

    return tmp_path

@patch("sys.argv", ["inference.py"])
def test_inference_script(mock_inference_data, monkeypatch, capsys):
    """
    Test that inference.py loads the trained model, reads new_data.csv,
    prints "Inference Results:" and per-row predictions.
    """
    # 1. Setup
    monkeypatch.chdir(mock_inference_data)

    # 2. Exercise
    inference_main()

    # 3. Verify
    captured = capsys.readouterr().out
    assert "Model loaded from ml/models/trained_model.joblib" in captured, (
        "Expected message about loading model was not found in output."
    )
    assert "Inference Results:" in captured, (
        "Expected 'Inference Results:' in output."
    )
    # We expect to see lines like "Row 0: X"
    # Just check if "Row 0:" appears
    assert "Row 0:" in captured or "Row 1:" in captured, (
        "Expected row predictions were not printed."
    )

    print("Test inference_script passed.")

@patch("sys.argv", ["inference.py"])
def test_inference_with_scaler(mock_inference_data, monkeypatch, capsys):
    """
    If a scaler is present, inference.py should load it and apply to new data.
    We'll create a dummy scaler for this scenario and confirm it's loaded.
    """
    # 1. Place dummy scaler in ml/models
    scaler_path = mock_inference_data / "ml" / "models" / "scaler.joblib"
    from joblib import dump
    from sklearn.preprocessing import StandardScaler
    dummy_scaler = StandardScaler()
    dump(dummy_scaler, scaler_path)

    # 2. Run
    monkeypatch.chdir(mock_inference_data)
    inference_main()

    # 3. Verify
    captured = capsys.readouterr().out
    assert "Scaler loaded from ml/models/scaler.joblib" in captured, (
        "Expected mention of scaler loading was not found."
    )
    assert "Inference Results:" in captured, "Expected inference results prompt was not found."
    print("Test inference_with_scaler passed.")
