import pytest
from Engine.Validators import Email

def test_email_validator_accepts_value():
    v = Email() # because email checks if @ in String
    result = v("alice@gmail.com") # User data
    assert result is None

def test_email_validator_rejects_value():
    v = Email()  # because email checks if @ in String
    result = v("alicegmail.com")  # User data
    assert result.code == "Email"
