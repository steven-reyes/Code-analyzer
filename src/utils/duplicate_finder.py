# src/utils/duplicate_finder.py

import os
import hashlib
from typing import Dict, Any

def analyze_duplicates(project_path: str) -> Dict[str, Any]:
    """
    Detects duplicate files by comparing checksums of all files.
    Returns a list of sets, where each set contains paths of duplicate files.
    """
    file_map = {}  # hash -> list of paths
    duplicates = []

    for root, dirs, files in os.walk(project_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            # We'll skip extremely large files or binary if needed, but here's a naive approach:
            try:
                with open(full_path, "rb") as f:
                    file_data = f.read()
                file_hash = hashlib.md5(file_data).hexdigest()
                file_map.setdefault(file_hash, []).append(full_path)
            except OSError:
                pass

    for file_hash, paths in file_map.items():
        if len(paths) > 1:
            duplicates.append(paths)

    return {"duplicates": duplicates}
