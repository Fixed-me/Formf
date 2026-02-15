import pytest
from Engine.Validators import Min

def test_min_validator_accepts_value():
    v = Min(5) # Form
    result = v(5) # User data
    assert result is None

def test_min_validator_rejects_value():
    v = Min(10) # Form
    result = v(5) # User data
    assert result.code == "Min"
