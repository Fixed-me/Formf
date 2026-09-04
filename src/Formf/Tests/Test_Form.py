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


def test_requiredif_tuple_not_empty():
    class MyForm(Form):
        name = String(required=False)
        age = Integer(requiredif=("name", True))

    form = MyForm({"name": "Alice"})
    assert not form.is_valid()
    assert "age" in form.errors


def test_requiredif_tuple_specific_value():
    class MyForm(Form):
        status = String(required=False)
        note = String(requiredif=("status", "approved"))

    form = MyForm({"status": "approved"})
    assert not form.is_valid()
    assert "note" in form.errors


def test_requiredif_dict_multiple_fields_any_equals():
    class MyForm(Form):
        role = String(required=False)
        plan = String(required=False)
        reason = String(requiredif={"fields": ["role", "plan"], "equals": "pro", "mode": "any"})

    form = MyForm({"role": "user", "plan": "pro"})
    assert not form.is_valid()
    assert "reason" in form.errors


def test_requiredif_dict_multiple_fields_all_not_empty():
    class MyForm(Form):
        first_name = String(required=False)
        last_name = String(required=False)
        nickname = String(requiredif={"fields": ["first_name", "last_name"], "not_empty": True, "mode": "all"})

    form = MyForm({"first_name": "Ada", "last_name": "Lovelace"})
    assert not form.is_valid()
    assert "nickname" in form.errors


def test_requiredif_dict_empty_condition():
    class MyForm(Form):
        middle_name = String(required=False)
        suffix = String(requiredif={"field": "middle_name", "is_empty": True})

    form = MyForm({})
    assert not form.is_valid()
    assert "suffix" in form.errors
