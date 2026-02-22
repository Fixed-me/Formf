# tests/Test_Form.py

import pytest
from Formf.Core.Form import Form
from Formf.fields.String import String
from Formf.fields.Integer import Integer

def test_form_requiredif():
    class MyForm(Form):
        name = String(required=True)
        age = Integer(requiredif=lambda form: form.cleaned_data.get("name") == "Alice")

    data = {"name": "Alice"}
    form = MyForm(data)
    assert not form.is_valid()
    assert "age" in form.errors

def test_form_valid_input():
    class MyForm(Form):
        name = String(required=True)
        age = Integer(required=False)

    data = {"name": "Alice", "age": 30}
    form = MyForm(data)
    assert form.is_valid()
    assert form.errors == {}
    assert form.cleaned_data == {"name": "Alice", "age": 30}


def test_form_optional_field_missing():
    class MyForm(Form):
        name = String(required=True)
        age = Integer(required=False)

    data = {"name": "Bob"}
    form = MyForm(data)
    assert form.is_valid()
    assert form.cleaned_data == {"name": "Bob"}

def test_form_invalid_field():
    class MyForm(Form):
        name = String(minlength=5)
        age = Integer()

    data = {"name": "abc", "age": "x"}
    form = MyForm(data)
    assert not form.is_valid()
    assert "name" in form.errors
    assert "age" in form.errors
    # cleaned_data should only have valid fields
    assert "name" not in form.cleaned_data
    assert "age" not in form.cleaned_data


