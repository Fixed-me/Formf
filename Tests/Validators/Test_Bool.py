import pytest
from Engine.Validators import Bool

def test_bool_validator_accepts_value():
    v = Bool(True) # Form
    result = v(True) # User data
    assert result is None

def test_bool_validator_rejects_value():
    v = Bool(False) # Form
    result = v(True) # User data
    assert result.code == "Bool"
