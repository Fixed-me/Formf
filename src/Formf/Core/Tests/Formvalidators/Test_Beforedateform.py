import pytest
from Formf.Core.Form import Form
from Formf.fields.String import String
from Formf.formvalidators import BeforeDate


def test_form_beforedate_validator_rejects_mismatch():
    class RegisterForm(Form):
        Date1 = String()
        Date2 = String()
        form_validators = [BeforeDate("Date1", "Date2")]

    form = RegisterForm({"Date1": "10.01.2020", "Date2": "09.01.2020"})

    assert not form.is_valid()
    assert "__all__" in form.errors
    assert form.errors["__all__"][0]["code"] == "BeforeDateForm"


def test_form_beforedate_validator_accepts_match():
    class RegisterForm(Form):
        Date1 = String()
        Date2 = String()
        form_validators = [BeforeDate("Date1", "Date2")]

    form = RegisterForm({"Date1": "09.01.2020", "Date2": "10.01.2020"})

    assert form.is_valid()
    assert form.errors == {}