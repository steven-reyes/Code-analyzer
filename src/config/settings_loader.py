import json
import os

def load_settings() -> dict:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    settings_path = os.path.join(current_dir, "settings.json")
    secrets_path = os.path.join(current_dir, "secrets.json")

    config = {}
    # Load main settings
    if os.path.isfile(settings_path):
        try:
            with open(settings_path, "r") as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {settings_path}: {e}")
    else:
        print("Warning: settings.json not found.")

    # Load secrets
    if os.path.isfile(secrets_path):
        try:
            with open(secrets_path, "r") as f:
                secrets = json.load(f)
            config.update(secrets)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {secrets_path}: {e}")
    else:
        print("Warning: secrets.json not found.")

    return config
