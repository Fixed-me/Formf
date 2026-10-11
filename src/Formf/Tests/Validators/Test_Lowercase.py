import pytest
from Formf.validators import Lowercase

def test_lowercase_validator_accepts_value():
    v = Lowercase(True) # Form
    result = v("aaa") # User data
    assert result is None

def test_lowercase_validator_rejects_value():
    v = Lowercase(True) # Form
    result = v("AAA") # User data
    assert result.code == "Lowercase"