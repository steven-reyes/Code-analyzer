# src/utils/security_scanner.py

import os
import re
from typing import Dict, Any

def analyze_security(project_path: str) -> Dict[str, Any]:
    """
    'Security' checks for:
      - Hardcoded secrets (expanded regex for password, private_key, etc.)
      - Known insecure functions (eval, exec).
    """
    issues = []

    # Examples: 'api_key = "something"', 'secret = "something"', 'password = "secretPass"'
    secret_pattern = re.compile(
        r"(?:api_key|secret|token|password|private_key|aws_access_key_id)\s*=\s*['\"](.+?)['\"]",
        re.IGNORECASE
    )

    # Insecure function usage: eval( ), exec( )
    insecure_func_pattern = re.compile(
        r"\beval\s*\(|\bexec\s*\(",
        re.IGNORECASE
    )

    for root, dirs, files in os.walk(project_path):
        for filename in files:
            # Check only .py files (could also check .env, .yaml, etc. if desired)
            if filename.endswith(".py"):
                full_path = os.path.join(root, filename)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    for i, line in enumerate(lines, start=1):
                        # Check for secrets
                        if secret_pattern.search(line):
                            issues.append(f"{full_path} Line {i}: Potential hardcoded secret => {line.strip()}")
                        # Check for insecure functions
                        if insecure_func_pattern.search(line):
                            issues.append(f"{full_path} Line {i}: Insecure function usage => {line.strip()}")
                except OSError:
                    pass

    return {"security_issues": issues}
