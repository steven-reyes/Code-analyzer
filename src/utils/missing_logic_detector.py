# src/utils/missing_logic_detector.py

import os
import re
from typing import Dict, List, Any

def _scan_file_for_patterns(filepath: str, patterns: List[str]) -> List[str]:
    """
    Reads file content line by line, returns lines that match any given patterns.
    """
    issues = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for i, line in enumerate(lines, start=1):
                for pat in patterns:
                    if re.search(pat, line):
                        issues.append(f"Line {i}: {line.strip()}")
    except OSError:
        pass
    return issues

def analyze_incomplete_logic(project_path: str) -> Dict[str, Any]:
    """
    Detects lines with 'TODO', 'pass', or 'NotImplementedError' in all .py files under project_path.
    Returns a dictionary with key 'incomplete_logic' mapping file paths to line lists.
    """
    patterns = [r"\bTODO\b", r"\bpass\b", r"\bNotImplementedError\b"]
    incomplete_issues = {}

    for root, dirs, files in os.walk(project_path):
        for filename in files:
            if filename.endswith(".py"):
                full_path = os.path.join(root, filename)
                matches = _scan_file_for_patterns(full_path, patterns)
                if matches:
                    incomplete_issues[full_path] = matches

    return {"incomplete_logic": incomplete_issues}
