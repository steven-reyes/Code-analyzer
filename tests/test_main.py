# src/main.py

import pytest
from unittest.mock import patch, MagicMock

# Since main.py imports from src, adjust the import path accordingly
from src.main import main

@patch("src.main.load_settings")
@patch("src.main.read_file")
@patch("src.main.ChatGPTClient")
@patch("src.main.app")
def test_main_flow(mock_app, mock_chatgpt, mock_read_file, mock_load_settings, capsys):
    """
    Test the main function end-to-end with mocks to prevent external I/O.
    """
    
    # 1. Setup Mocks
    mock_load_settings.return_value = {"setting_key": "setting_value"}
    
    mock_read_file.return_value = "Test file content"
    
    # ChatGPT Mock
    mock_chatgpt_instance = MagicMock()
    mock_chatgpt_instance.send_message.return_value = "Mocked ChatGPT Response"
    mock_chatgpt.return_value = mock_chatgpt_instance
    
    # Mock the Flask app's run method to prevent actually starting the server
    mock_app.run = MagicMock()

    # 2. Exercise
    main()

    # 3. Verify
    # Check load_settings was called
    mock_load_settings.assert_called_once()

    # Check read_file was called with "some_data_file.txt"
    mock_read_file.assert_called_once_with("some_data_file.txt")

    # Check ChatGPT was called with the expected message
    mock_chatgpt_instance.send_message.assert_called_once_with(
        "What can you tell me about the project structure?",
        context="You are ChatGPT-01. Provide insights on code structure."
    )

    # Check Flask app was started
    mock_app.run.assert_called_once_with(host="127.0.0.1", port=5000, debug=True)

    # Capture the stdout
    captured = capsys.readouterr().out
    
    # Optionally, confirm certain prints/strings appear
    assert "Hello, Alice! Welcome to the Code Analyzer." in captured
    assert "File read successfully!" in captured
    assert "Mocked ChatGPT Response" in captured
    assert "setting_key" in captured  # from printed JSON config
