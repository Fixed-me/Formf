import pytest
from Formf.validators import Uppercase

def test_uppercase_validator_accepts_value():
    v = Uppercase(True) # Form
    result = v("AAAA") # User data
    assert result is None

def test_uppercase_validator_rejects_value():
    v = Uppercase(True) # Form
    result = v("aaaaaa") # User data
    assert result.code == "Uppercase"