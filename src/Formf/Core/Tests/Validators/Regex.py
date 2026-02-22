import pytest
from Formf.validators import Regex

def test_regex_validator_accepts_value():
    v = Regex("^[^@]+@[^@]+\.[^@]+$") # Form
    result = v("alice@example.com") # User data
    assert result is None

def test_regex_validator_rejects_value():
    v = Regex("^[^@]+@[^@]+\.[^@]+$") # Form
    result = v("alice.example.com") # User data
    assert result.code == "Regex"