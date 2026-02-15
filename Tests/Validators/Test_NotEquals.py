import pytest
from Engine.Validators import NotEquals

def test_notequals_validator_accepts_value():
    v = NotEquals(5) # Form
    result = v("aaaa") # User data
    assert result is None

def test_notequals_validator_rejects_value():
    v = NotEquals(5) # Form
    result = v(5) # User data
    assert result.code == "NotEquals"