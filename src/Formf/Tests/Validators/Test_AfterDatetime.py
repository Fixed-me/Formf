import pytest
from Formf.validators import After

def test_after_validator_accepts_value():
    v = After("2026-01-01") # Form
    result = v("2027-01-01") # User data
    assert result is None

def test_after_validator_rejects_value():
    v = After("2027-01-01") # Form
    result = v("2026-01-01") # User data
    assert result.code == "AfterDatetime"
