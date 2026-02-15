import pytest
from Engine.Validators import Choices

def test_choices_validator_accepts_value():
    v = Choices([True, 1, "Test"]) # Form
    result = v([True, 1, "Test"]) # User data
    assert result is None

def test_choices_validator_rejects_value():
    v = Choices([True, 1, "Test"]) # Form
    result = v([True, 1]) # User data
    assert result.code == "Choices"
