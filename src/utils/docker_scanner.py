# src/utils/docker_scanner.py

import os
import re
from typing import Dict, Any

def analyze_docker_setup(project_path: str) -> Dict[str, Any]:
    """
    Checks for Dockerfile and docker-compose.yml and looks for:
      - Placeholders (TODO, PLACEHOLDER)
      - Some best-practice checks (example: if 'apt-get update' is missing a '&& apt-get upgrade', etc.)

    Returns a dict:
      {
        "dockerfile_found": bool,
        "docker_compose_found": bool,
        "docker_issues": list of strings
      }
    """
    results = {
        "dockerfile_found": False,
        "docker_compose_found": False,
        "docker_issues": []
    }

    dockerfile = os.path.join(project_path, "Dockerfile")
    if os.path.isfile(dockerfile):
        results["dockerfile_found"] = True
        dockerfile_issues = _scan_dockerfile(dockerfile)
        results["docker_issues"].extend(dockerfile_issues)

    compose = os.path.join(project_path, "docker-compose.yml")
    if os.path.isfile(compose):
        results["docker_compose_found"] = True
        compose_issues = _scan_docker_compose(compose)
        results["docker_issues"].extend(compose_issues)

    return results

def _scan_dockerfile(dockerfile_path: str) -> list:
    """
    Reads Dockerfile line by line, checking for:
      - 'TODO' or 'PLACEHOLDER'
      - Basic best practices like apt-get usage
    """
    issues = []
    placeholder_pattern = re.compile(r"(TODO|PLACEHOLDER)", re.IGNORECASE)

    # Example best-practices to check:
    # 1) If line has "apt-get update" but doesn't have "&& apt-get upgrade"
    # 2) If there's no explicit 'FROM' in the top lines

    found_from = False
    try:
        with open(dockerfile_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for i, line in enumerate(lines, start=1):
                if "FROM" in line.upper():
                    found_from = True
                if placeholder_pattern.search(line):
                    issues.append(f"{dockerfile_path} line {i}: Found placeholder => {line.strip()}")
                if "apt-get update" in line and "&&" not in line:
                    issues.append(f"{dockerfile_path} line {i}: 'apt-get update' not chained with 'apt-get upgrade' or similar best practice.")
            
            if not found_from:
                issues.append(f"{dockerfile_path}: No 'FROM' instruction found (best practice is to define base image).")
    except OSError as e:
        issues.append(f"Error reading Dockerfile: {e}")

    return issues

def _scan_docker_compose(compose_path: str) -> list:
    """
    Scans docker-compose.yml for placeholders or typical issues.
    """
    issues = []
    placeholder_pattern = re.compile(r"(TODO|PLACEHOLDER)", re.IGNORECASE)
    try:
        with open(compose_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for i, line in enumerate(lines, start=1):
                if placeholder_pattern.search(line):
                    issues.append(f"{compose_path} line {i}: Found placeholder => {line.strip()}")
                # Add more checks if needed
    except OSError as e:
        issues.append(f"Error reading docker-compose.yml: {e}")

    return issues
