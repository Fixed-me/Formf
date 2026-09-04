import pytest
from Formf.validators import NotInList

def test_notinlist_validator_accepts_value():
    v = NotInList((5,6,7,"HI")) # Form
    result = v("aaaaaa") # User data
    assert result is None

def test_minlength_validator_rejects_value():
    v = NotInList((5,6,7,"HI")) # Form
    result = v("HI") # User data
    assert result.code == "NoInList"