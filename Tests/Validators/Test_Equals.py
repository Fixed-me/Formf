import pytest
from Engine.Validators import Equals

def test_equals_validator_accepts_value():
    v = Equals(5) # Form
    result = v(5) # User data
    assert result is None

def test_equals_validator_rejects_value():
    v = Equals(10) # Form
    result = v(5) # User data
    assert result.code == "Equals"