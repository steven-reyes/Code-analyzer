# src/utils/file_structure_scanner.py

import os
from typing import Dict, Any

def analyze_file_structure(project_path: str) -> Dict[str, Any]:
    """
    Recursively traverses the project, capturing file paths, sizes.
    Returns a dict with aggregated stats and file details.
    """
    total_files = 0
    total_size = 0
    file_details = []

    for root, dirs, files in os.walk(project_path):
        for file_name in files:
            total_files += 1
            full_path = os.path.join(root, file_name)
            try:
                size = os.path.getsize(full_path)
                total_size += size
                file_details.append({
                    "path": full_path,
                    "size": size
                })
            except OSError:
                file_details.append({
                    "path": full_path,
                    "size": "Unknown (OS Error)"
                })

    return {
        "total_files": total_files,
        "total_size_bytes": total_size,
        "file_details": file_details
    }
