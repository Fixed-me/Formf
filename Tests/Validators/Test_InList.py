import pytest
from Engine.Validators import InList

def test_inlist_validator_accepts_value():
    v = InList((5,6,7,"HI")) # Form
    result = v(5) # User data
    assert result is None

def test_inlist_validator_rejects_value():
    v = InList((5,6,7,"HI")) # Form
    result = v(2) # User data
    assert result.code == "InList"