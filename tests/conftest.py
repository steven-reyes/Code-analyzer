# tests/conftest.py

import os
import pytest

# If you import Flask `app` directly from src/ui/app.py:
# from src.ui.app import app as flask_app

# OR if you have a factory function in src/ui/app.py that creates the app:
# from src.ui.app import create_app


@pytest.fixture(scope="session", autouse=True)
def setup_test_env(monkeypatch):
    """
    This fixture runs once per test session (scope="session").
    It sets environment variables or other global test configurations
    needed by your application.

    - We use 'monkeypatch' to override or inject environment variables.
    - Good place for global setup that all tests rely on.

    The 'autouse=True' means this fixture is automatically used in every test
    session without having to import or reference it explicitly.

    Example usage:
        1) Setting environment vars required by the code.
        2) Overriding config for testing (db paths, API keys).
    """
    # Example environment variables
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("SECRET_KEY", "my_test_secret_key")

    # If your application reads a .env file or other config,
    # you can override relevant variables here (e.g. DB_HOST, DB_PORT, etc.).

    yield
    # Teardown logic (if any) goes here.
    # e.g., resetting environment variables, cleaning up global resources, etc.


@pytest.fixture(scope="session")
def flask_app():
    """
    Creates (or imports) the Flask application to be used in tests.

    1) If you have a Flask "app factory" in src/ui/app.py:
       from src.ui.app import create_app
       and then do:
         config = {"TESTING": True, "DEBUG": False, ...}
         app = create_app(config)
         return app

    2) If your app is a single, globally defined 'app' in src/ui/app.py:
       from src.ui.app import app
       return app

    We'll show a default approach #2 below, but feel free to adapt.
    """
    # Example 1: App factory approach
    # from src.ui.app import create_app
    # test_config = {
    #     "TESTING": True,
    #     "DEBUG": False,
    #     # e.g., "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    # }
    # flask_app = create_app(test_config)
    # return flask_app

    # Example 2: Global 'app' import
    from src.ui.app import app
    # Optionally override app.config here, e.g.:
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    return app


@pytest.fixture
def client(flask_app):
    """
    Provides a Flask test client for making HTTP requests to your routes
    without starting the real server.

    Usage in a test function:
        def test_some_route(client):
            response = client.get('/')
            assert response.status_code == 200

    'flask_app.test_client()' is a context manager that yields a client
    you can use to perform GET, POST, etc.
    """
    with flask_app.test_client() as test_client:
        yield test_client


@pytest.fixture
def sample_data():
    """
    Example fixture containing sample data that can be reused across
    multiple tests.

    This can be data in the form of a dictionary, a list, or any structure
    your tests typically need.

    Example usage in a test:
        def test_data_processing(sample_data):
            assert sample_data["id"] == 123
    """
    return {
        "id": 123,
        "name": "TestRecord",
        "description": "Sample data for testing."
    }
