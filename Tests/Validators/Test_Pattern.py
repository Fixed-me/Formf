import pytest
from Engine.Validators import Pattern

def test_pattern_validator_accepts_value():
    v = Pattern("numeric")
    result = v("123")
    assert result is None

def test_pattern_validator_rejects_value():
    v = Pattern("numeric")
    result = v("hi")
    assert result.code == "Pattern"
