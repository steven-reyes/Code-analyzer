# src/utils/env_file_scanner.py

import os
import re
from typing import Dict, Any

ENV_LINE_PATTERN = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(['\"]?)(?P<value>.*)\2$")

def analyze_env_file(project_path: str) -> Dict[str, Any]:
    """
    Checks if there's a .env file, tries to parse environment variables,
    including quoted values. Also stores comment lines.
    """
    env_path = os.path.join(project_path, ".env")
    result = {
        "env_found": False,
        "env_vars": [],
        "comments": [],
        "potential_secrets": []
    }

    if os.path.isfile(env_path):
        result["env_found"] = True
        with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for line in lines:
                raw_line = line.strip()
                if not raw_line or raw_line.startswith("#"):
                    result["comments"].append(raw_line)
                    continue

                match = ENV_LINE_PATTERN.match(raw_line)
                if match:
                    key = match.group("key")
                    value = match.group("value")
                    # Remove surrounding quotes if any
                    value = value.strip("'\"")
                    result["env_vars"].append({"name": key, "value": value})

                    # Optional synergy with security scanning: 
                    # If key looks like something sensitive, add to potential_secrets
                    if "secret" in key.lower() or "token" in key.lower():
                        result["potential_secrets"].append(f"{key} might be sensitive.")
                else:
                    # If we can't parse it with the pattern, treat as comment or unrecognized
                    result["comments"].append(raw_line)

    return result
