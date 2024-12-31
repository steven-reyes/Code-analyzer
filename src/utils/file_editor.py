import os

def edit_file(filepath, new_content):
    """
    Overwrites or updates the specified file with new_content.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return f"File {filepath} successfully updated."

def generate_output_file(filepath, new_content, output_dir="output/updated_files"):
    """
    Creates the updated file in the output directory instead of in-place.
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(filepath)
    new_path = os.path.join(output_dir, filename)
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return f"File generated at {new_path}"
