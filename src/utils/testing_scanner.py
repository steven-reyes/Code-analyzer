# src/utils/testing_scanner.py

import os
from typing import Dict, Any

def analyze_testing_setup(project_path: str) -> Dict[str, Any]:
    """
    Scans for evidence of testing frameworks or coverage configs:
      - pytest usage
      - unittest usage
      - nose or tox (optional)
      - coverage config files
      - cypress folder & cypress config
    """
    test_info = {
        "pytest_found": False,
        "unittest_found": False,
        "nose_found": False,
        "tox_found": False,
        "coverage_files": [],
        "cypress_found": False,
        "cypress_config_found": False,
        "test_directories": []
    }

    # 1) Check for cypress directory
    cypress_dir = os.path.join(project_path, "cypress")
    if os.path.isdir(cypress_dir):
        test_info["cypress_found"] = True
        # Also check for cypress.json or cypress.config.js in root
        cypress_json = os.path.join(project_path, "cypress.json")
        cypress_config_js = os.path.join(project_path, "cypress.config.js")
        if os.path.isfile(cypress_json) or os.path.isfile(cypress_config_js):
            test_info["cypress_config_found"] = True

    # 2) Look for coverage files
    possible_coverage_files = ["coverage.xml", ".coveragerc", "coverage", "coverage-report"]
    for file_name in possible_coverage_files:
        fp = os.path.join(project_path, file_name)
        if os.path.exists(fp):
            test_info["coverage_files"].append(file_name)

    # 3) Walk project to detect usage of various test frameworks
    for root, dirs, files in os.walk(project_path):
        # If we see a directory named 'tests', record it
        if root.endswith("tests"):
            test_info["test_directories"].append(root)

        for filename in files:
            if filename.endswith(".py"):
                full_path = os.path.join(root, filename)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    # basic checks
                    if "import pytest" in content:
                        test_info["pytest_found"] = True
                    if "import unittest" in content or "from unittest" in content:
                        test_info["unittest_found"] = True
                    if "import nose" in content or "from nose" in content:
                        test_info["nose_found"] = True
                    if "import tox" in content or "from tox" in content:
                        test_info["tox_found"] = True
                except OSError:
                    pass

    return test_info
