# tests/e2e/test_end_to_end_flow.py

import pytest
import subprocess
import time
import requests
import os


@pytest.mark.e2e
def test_end_to_end_server_flow():
    """
    Example E2E test: 
    1. Start the Python server in a subprocess
    2. Make requests to it and verify the responses
    3. Shut down the server
    
    Assumptions:
    - main.py starts a Flask server listening on localhost:5000
    - The home endpoint returns "Welcome to Code Analyzer"
    """
    # Optionally set environment variables before starting the server
    # os.environ["APP_ENV"] = "e2e_test"
    
    process = None
    try:
        # 1. Start the Flask server as a subprocess
        process = subprocess.Popen(
            ["python", "src/main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 2. Wait for server to spin up (could also poll the port in a loop)
        time.sleep(2)

        # 3. Make a request to the server
        response = requests.get("http://localhost:5000/")
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

        # Suppose the home endpoint returns "Welcome to Code Analyzer"
        assert "Welcome to Code Analyzer" in response.text, "Home page did not contain expected text."

        # (Optional) Test additional endpoints
        # response_2 = requests.get("http://localhost:5000/some-other-endpoint")
        # assert response_2.status_code == 200
        # assert "Some expected text" in response_2.text

    finally:
        # 4. Terminate the server process
        if process:
            process.terminate()
            process.wait()
            # Optionally, capture and inspect logs if needed
            # stdout, stderr = process.communicate()
            # print("Server stdout:", stdout)
            # print("Server stderr:", stderr)


@pytest.mark.e2e
def test_end_to_end_cli_flow():
    """
    Another E2E scenario: 
    1. Run your application as a CLI (using python src/main.py)
    2. Check its console output and return code
    
    Assumptions:
    - main.py prints "Main application is running..." or some identifiable log
    - The script exits with code 0 on success.
    """
    # If you have environment variables for CLI mode, set them here
    # os.environ["CLI_MODE"] = "true"

    # Execute the main script
    result = subprocess.run(
        ["python", "src/main.py"],
        capture_output=True,
        text=True
    )

    # 1. Check stdout contains specific text
    assert "Main application is running" in result.stdout, (
        "CLI output does not contain the expected text."
    )

    # 2. Check process exit code
    assert result.returncode == 0, (
        f"CLI returned a non-zero exit code: {result.returncode}"
    )

    # (Optional) Parse or analyze the output further
    # For example, if the script prints JSON or logs certain messages:
    # assert "ChatGPT-01 Response" in result.stdout
