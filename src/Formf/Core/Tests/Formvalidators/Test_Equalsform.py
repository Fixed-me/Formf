import pytest
from Formf.Core.Form import Form
from Formf.fields.String import String
from Formf.formvalidators import Equals


def test_form_equals_validator_rejects_mismatch():
    class RegisterForm(Form):
        password = String()
        password_repeat = String()
        form_validators = [Equals("password", "password_repeat")]

    form = RegisterForm({"password": "abc123", "password_repeat": "abc124"})

    assert not form.is_valid()
    assert "__all__" in form.errors
    assert form.errors["__all__"][0]["code"] == "Equalsform"


def test_form_equals_validator_accepts_match():
    class RegisterForm(Form):
        password = String()
        password_repeat = String()
        form_validators = [Equals("password", "password_repeat")]

    form = RegisterForm({"password": "abc123", "password_repeat": "abc123"})

    assert form.is_valid()
    assert form.errors == {}
