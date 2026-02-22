# tests/Test_Field.py
import pytest
from Formf.Fields import String

def test_string_field_required():
    field = String(required=True)
    value, errors = field.clean(None)
    assert value is None
    assert errors[0].code == "required"

def test_string_field_nullable():
    field = String(nullable=False)
    value, errors = field.clean(None)
    assert errors[0].code == "nullable"


def test_string_field_blank():
    field = String(blank=False)
    value, errors = field.clean("")
    assert errors[0].code == "blank"

