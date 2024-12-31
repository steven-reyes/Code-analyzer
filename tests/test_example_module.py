import pytest
from src.modules.example_module import greet_user

def test_greet_user_regular_name():
    """
    Test that greet_user returns the correct string with a typical name.
    """
    result = greet_user("Alice")
    assert result == "Hello, Alice! Welcome to the Code Analyzer."

def test_greet_user_empty_string():
    """
    Test greet_user handles an empty string.
    """
    result = greet_user("")
    assert result == "Hello, ! Welcome to the Code Analyzer."

@pytest.mark.parametrize("name", [123, None, True])
def test_greet_user_unexpected_input(name):
    """
    Test greet_user with non-string input. This might raise an exception,
    or handle it in a specific way, depending on your design.
    """
    # If you expect an exception:
    with pytest.raises(TypeError):
        greet_user(name)
    # Otherwise, if your code is more permissive,
    # you might assert something else, e.g.:
    # result = greet_user(str(name))
    # assert "Hello" in result
