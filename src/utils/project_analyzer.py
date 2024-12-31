# src/utils/project_analyzer.py

import json
import os
import sys
from typing import Dict, Any, List, Optional

# Import each specialized scanner
from src.utils.file_structure_scanner import analyze_file_structure
from src.utils.requirements_scanner import analyze_requirements
from src.utils.docker_scanner import analyze_docker_setup
from src.utils.ml_scanner import analyze_ml_workflow
from src.utils.missing_logic_detector import analyze_incomplete_logic
from src.utils.env_file_scanner import analyze_env_file
from src.utils.security_scanner import analyze_security
from src.utils.duplicate_finder import analyze_duplicates
from src.utils.logging_scanner import analyze_logging_and_monitoring
from src.utils.testing_scanner import analyze_testing_setup


def analyze_project(
    project_path: str,
    skip_dirs: Optional[List[str]] = None,
    skip_large_files: bool = False,
    large_file_threshold_mb: int = 50
) -> Dict[str, Any]:
    """
    Coordinates all sub-analyses by calling each specialized scanner.
    Returns a consolidated report as a dictionary.

    :param project_path: Path to the project directory to analyze.
    :param skip_dirs: Optional list of directory names to skip (e.g., ['node_modules', '.git', '__pycache__']).
    :param skip_large_files: If True, some scanners may skip files above 'large_file_threshold_mb'.
    :param large_file_threshold_mb: The file size threshold in MB if skipping large files.
    """

    # Validate project_path
    if not os.path.isdir(project_path):
        return {
            "error": f"Provided path '{project_path}' is not a valid directory.",
            "project_path": project_path
        }

    # If skipping directories, set it up globally, though each scanner
    # might handle it differently if you integrate that logic.
    # Currently, most scanners read the entire tree, so you'd incorporate
    # skip logic within them if needed.

    # 1. File structure
    file_structure = analyze_file_structure(project_path)

    # 2. Requirements
    requirements_info = analyze_requirements(project_path)

    # 3. Docker setup
    docker_info = analyze_docker_setup(project_path)

    # 4. ML workflow
    ml_info = analyze_ml_workflow(project_path)

    # 5. Incomplete logic
    incomplete_logic = analyze_incomplete_logic(project_path)

    # 6. .env checks
    env_info = analyze_env_file(project_path)

    # 7. Security checks
    security_info = analyze_security(project_path)

    # 8. Duplicate or redundant files
    duplicates_info = analyze_duplicates(project_path)

    # 9. Logging & Monitoring
    logging_info = analyze_logging_and_monitoring(project_path)

    # 10. Testing & QA
    testing_info = analyze_testing_setup(project_path)

    # Consolidate everything
    report = {
        "project_path": project_path,
        "file_structure": file_structure,
        "requirements": requirements_info,
        "docker_setup": docker_info,
        "ml_workflow": ml_info,
        "incomplete_logic": incomplete_logic,
        "env_file": env_info,
        "security": security_info,
        "duplicates": duplicates_info,
        "logging_monitoring": logging_info,
        "testing": testing_info
    }

    # If skip_large_files is True, you might do a post-scan pass in each dictionary
    # to remove or mark large files. But that logic must be integrated inside each scanner.

    return report


if __name__ == "__main__":
    # Basic CLI usage
    if len(sys.argv) < 2:
        print("Usage: python project_analyzer.py /path/to/project [skip_dir1,skip_dir2,...]")
        sys.exit(1)

    project_path = sys.argv[1]
    skip_dirs_list = []

    # Optional: parse second argument for skip dirs
    if len(sys.argv) > 2:
        skip_dirs_list = sys.argv[2].split(",")

    # Perform analysis
    results = analyze_project(project_path, skip_dirs=skip_dirs_list)

    # Print as JSON
    print(json.dumps(results, indent=2))
