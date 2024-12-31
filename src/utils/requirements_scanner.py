# src/utils/requirements_scanner.py

import os
import re
from typing import Dict, Any, List, Tuple

VERSION_PATTERN = re.compile(
    r"^(?P<name>[A-Za-z0-9_\-\.]+)(?P<specifier>==|>=|<=|~=|!=|>|<)?(?P<version>[0-9a-zA-Z\.\-]*)$"
)

def analyze_requirements(project_path: str) -> Dict[str, Any]:
    results = {
        "requirements_txt": {
            "found": False,
            "packages": [],
            "missing_versions": [],
            "duplicates": []
        },
        "environment_yml": {
            "found": False,
            "packages": [],
            "missing_versions": [],
            "duplicates": []
        }
    }

    req_path = os.path.join(project_path, "requirements.txt")
    if os.path.isfile(req_path):
        results["requirements_txt"]["found"] = True
        lines = _read_lines(req_path)
        packages, missing, duplicates = _parse_requirements_txt(lines)
        results["requirements_txt"]["packages"] = packages
        results["requirements_txt"]["missing_versions"] = missing
        results["requirements_txt"]["duplicates"] = duplicates

    env_yml_path = os.path.join(project_path, "environment.yml")
    if os.path.isfile(env_yml_path):
        results["environment_yml"]["found"] = True
        lines = _read_lines(env_yml_path)
        packages, missing, duplicates = _parse_environment_yml(lines)
        results["environment_yml"]["packages"] = packages
        results["environment_yml"]["missing_versions"] = missing
        results["environment_yml"]["duplicates"] = duplicates

    return results

def _read_lines(filepath: str) -> List[str]:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f.readlines()]

def _parse_requirements_txt(lines: List[str]) -> Tuple[List[dict], List[str], List[str]]:
    packages = []
    name_counts = {}
    missing_versions = []
    duplicates = []

    for line in lines:
        if not line or line.startswith("#"):
            continue

        match = VERSION_PATTERN.match(line)
        if match:
            name = match.group("name")
            specifier = match.group("specifier") or ""
            version = match.group("version") or ""
            packages.append({
                "name": name,
                "specifier": specifier,
                "version": version if version else None
            })
            name_counts[name] = name_counts.get(name, 0) + 1

            if not version:
                missing_versions.append(line)
        else:
            packages.append({"name": line, "specifier": None, "version": None})
            missing_versions.append(line)

    for pkg_name, count in name_counts.items():
        if count > 1:
            duplicates.append(pkg_name)

    return packages, missing_versions, duplicates

def _parse_environment_yml(lines: List[str]) -> Tuple[List[dict], List[str], List[str]]:
    packages = []
    name_counts = {}
    missing_versions = []
    duplicates = []

    in_deps = False
    for line in lines:
        if line.lower().startswith("dependencies:"):
            in_deps = True
            continue

        if in_deps and line.startswith("- "):
            pkg_line = line[2:].strip()
            if pkg_line.startswith("pip:"):
                continue

            match = VERSION_PATTERN.match(pkg_line)
            if match:
                name = match.group("name")
                specifier = match.group("specifier") or ""
                version = match.group("version") or ""
                packages.append({
                    "name": name,
                    "specifier": specifier,
                    "version": version if version else None
                })
                name_counts[name] = name_counts.get(name, 0) + 1

                if not version:
                    missing_versions.append(pkg_line)
            else:
                packages.append({"name": pkg_line, "specifier": None, "version": None})
                missing_versions.append(pkg_line)

    for pkg_name, count in name_counts.items():
        if count > 1:
            duplicates.append(pkg_name)

    return packages, missing_versions, duplicates
