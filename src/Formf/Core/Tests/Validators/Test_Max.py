import pytest
from Formf.validators import Max

def test_max_validator_accepts_value():
    v = Max(5) # Form
    result = v(4) # User data
    assert result is None

def test_max_validator_rejects_value():
    v = Max(5) # Form
    result = v(6) # User data
    assert result.code == "Max"