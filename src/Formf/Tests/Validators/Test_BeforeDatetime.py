import pytest
from Formf.Validators import Before

def test_before_validator_accepts_value():
    v = Before("2027-01-01") # Form
    result = v("2026-01-01") # User data
    assert result is None

def test_before_validator_rejects_value():
    v = Before("2026-01-01") # Form
    result = v("2027-01-01") # User data
    assert result.code == "BeforeDatetime"
