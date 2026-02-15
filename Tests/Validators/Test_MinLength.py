import pytest
from Engine.Validators import MinLength

def test_minlength_validator_accepts_value():
    v = MinLength(5) # Form
    result = v("aaaaaa") # User data
    assert result is None

def test_minlength_validator_rejects_value():
    v = MinLength(5) # Form
    result = v("aaaa") # User data
    assert result.code == "Min-length"