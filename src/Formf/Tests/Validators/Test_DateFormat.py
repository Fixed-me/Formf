import pytest
from Formf.Validators import Dateformat

def test_dateformat_validator_accepts_value():
    v = Dateformat("YYYY-MM-DD") # Form
    result = v("2026-01-01") # User data
    assert result is None

def test_dateformat_validator_rejects_value():
    v = Dateformat("YYYY-MM-DD") # Form
    result = v("01-01-2026") # User data
    assert result.code == "Dateformat"
