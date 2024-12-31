# src/utils/logging_scanner.py

import os
import re
from typing import Dict, Any

def analyze_logging_and_monitoring(project_path: str) -> Dict[str, Any]:
    """
    Scans for usage of Python's logging module or references to third-party monitoring tools.
    Checks if 'logging.basicConfig' or 'logging.getLogger' is used, or if Sentry/Datadog calls appear.
    """
    logging_usage = []
    monitoring_usage = []
    
    # Simple patterns
    logging_pattern = re.compile(r"\blogging\.(basicConfig|getLogger)\b")
    sentry_pattern = re.compile(r"\bimport\s+sentry_sdk\b|\bsentry_sdk.init\b")
    datadog_pattern = re.compile(r"\bimport\s+datadog\b|\bimport\s+ddtrace\b")

    for root, dirs, files in os.walk(project_path):
        for filename in files:
            if filename.endswith(".py"):
                full_path = os.path.join(root, filename)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    for i, line in enumerate(lines, start=1):
                        if logging_pattern.search(line):
                            logging_usage.append(f"{full_path}:{i} => {line.strip()}")
                        if sentry_pattern.search(line):
                            monitoring_usage.append(f"{full_path}:{i} => {line.strip()}")
                        if datadog_pattern.search(line):
                            monitoring_usage.append(f"{full_path}:{i} => {line.strip()}")
                except OSError:
                    pass

    # Summary
    return {
        "logging_found": len(logging_usage) > 0,
        "logging_references": logging_usage,
        "monitoring_found": len(monitoring_usage) > 0,
        "monitoring_references": monitoring_usage
    }
