# src/utils/ml_scanner.py

import os
import json
from typing import Dict, Any, Tuple, List

def analyze_ml_workflow(project_path: str) -> Dict[str, Any]:
    """
    Checks the ml/ folder for presence of:
      - config files (model_config.json, dataset_config.json)
      - any .py scripts in ml/scripts/
      - .ipynb notebooks in ml/notebooks/

    Optionally, performs basic validation on model_config.json if found.
    """
    ml_folder = os.path.join(project_path, "ml")
    ml_result = {
        "ml_folder_found": False,
        "configs_found": [],
        "scripts_found": [],
        "notebooks_found": [],
        "model_config_valid": True,
        "validation_messages": []
    }

    if not os.path.isdir(ml_folder):
        return ml_result

    ml_result["ml_folder_found"] = True

    # 1) config folder
    config_folder = os.path.join(ml_folder, "config")
    if os.path.isdir(config_folder):
        model_cfg_path = os.path.join(config_folder, "model_config.json")
        dataset_cfg_path = os.path.join(config_folder, "dataset_config.json")

        if os.path.isfile(model_cfg_path):
            ml_result["configs_found"].append("model_config.json")
            is_valid, msgs = _validate_model_config(model_cfg_path)
            ml_result["model_config_valid"] = ml_result["model_config_valid"] and is_valid
            ml_result["validation_messages"].extend(msgs)

        if os.path.isfile(dataset_cfg_path):
            ml_result["configs_found"].append("dataset_config.json")

    # 2) scripts folder
    scripts_folder = os.path.join(ml_folder, "scripts")
    if os.path.isdir(scripts_folder):
        for filename in os.listdir(scripts_folder):
            if filename.endswith(".py"):
                ml_result["scripts_found"].append(filename)

    # 3) notebooks folder
    notebooks_folder = os.path.join(ml_folder, "notebooks")
    if os.path.isdir(notebooks_folder):
        for f in os.listdir(notebooks_folder):
            if f.endswith(".ipynb"):
                ml_result["notebooks_found"].append(f)

    return ml_result

def _validate_model_config(filepath: str) -> Tuple[bool, List[str]]:
    """
    Loads model_config.json and checks for required fields.
    Returns (is_valid, list_of_messages).
    """
    is_valid = True
    messages: List[str] = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Example checks: 'model_type' and 'hyperparameters' must exist
        if "model_type" not in data:
            is_valid = False
            messages.append("model_type is missing from model_config.json.")
        if "hyperparameters" not in data:
            is_valid = False
            messages.append("hyperparameters is missing from model_config.json.")
    except (OSError, json.JSONDecodeError) as e:
        is_valid = False
        messages.append(f"Error reading or parsing model_config.json: {str(e)}")

    return is_valid, messages
