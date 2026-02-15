import pytest
from Engine.Validators import MaxLength

def test_maxlength_validator_accepts_value():
    v = MaxLength(6) # Form
    result = v("aaaaa") # User data
    assert result is None

def test_maxlength_validator_rejects_value():
    v = MaxLength(6) # Form
    result = v("aaaaaaa") # User data
    assert result.code == "Max-length"