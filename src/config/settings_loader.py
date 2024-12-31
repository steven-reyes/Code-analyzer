# src/config/settings_loader.py

import json
import os

def load_settings() -> dict:
    """
    Loads settings from settings.json and secrets.json, then merges them.
    Returns a dictionary of combined config.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))

    settings_path = os.path.join(current_dir, "settings.json")
    secrets_path = os.path.join(current_dir, "secrets.json")

    config = {}
    # Load main settings
    if os.path.isfile(settings_path):
        with open(settings_path, "r") as f:
            config = json.load(f)
    else:
        print("Warning: settings.json not found.")

    # Load secrets
    if os.path.isfile(secrets_path):
        with open(secrets_path, "r") as f:
            secrets = json.load(f)
        # Merge secrets into main config
        config.update(secrets)
    else:
        print("Warning: secrets.json not found.")

    return config
