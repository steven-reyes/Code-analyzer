# scripts/generate_configs.py

import json
import os
import argparse

CONFIG_TEMPLATE = {
    "appName": "Code Analyzer",
    "version": "1.0.0",
    "database": {
        "host": "localhost",
        "port": 5432,
        "username": "default_user",
        "password": ""
    }
}

def main():
    """
    Example script to generate or update a settings.json based on environment variables
    or a default template.
    1. Reads env variables like DB_HOST, DB_PORT, DB_USER, DB_PASS
    2. Overwrites fields in CONFIG_TEMPLATE
    3. Writes config to src/config/settings.json (or user-defined path)
    """
    parser = argparse.ArgumentParser(description="Generate or update JSON configs.")
    parser.add_argument("--output", default="src/config/settings.json", help="Path to output config file.")
    args = parser.parse_args()

    output_path = args.output

    # Load environment variables
    env_host = os.getenv("DB_HOST", "localhost")
    env_port = os.getenv("DB_PORT", "5432")
    env_user = os.getenv("DB_USER", "default_user")
    env_pass = os.getenv("DB_PASS", "default_pass")

    # Populate template with env vars
    config = CONFIG_TEMPLATE.copy()
    config["database"]["host"] = env_host
    config["database"]["port"] = int(env_port)
    config["database"]["username"] = env_user
    config["database"]["password"] = env_pass

    # Optionally read more env vars like APP_NAME, VERSION, etc.
    # e.g., config["appName"] = os.getenv("APP_NAME", config["appName"])

    # Write the new config
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    print(f"Generated config file at {output_path}")

if __name__ == "__main__":
    main()
