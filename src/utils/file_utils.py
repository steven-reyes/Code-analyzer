# src/utils/file_utils.py

import os

def read_file(filepath: str) -> str:
    """
    Reads and returns the content of the given file.
    Returns an empty string if the file doesn't exist.
    """
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return ""

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def write_file(filepath: str, data: str):
    """
    Writes the provided data to the specified filepath.
    Creates the file if it doesn't exist.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data)
    print(f"Data written to {filepath}")
