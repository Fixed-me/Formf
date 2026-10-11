from Formf.fields.List import List
from Formf.validators.InList import InList


def test_list_field_membership_requires_in_list():
    field = List(listvalues=["a", "b"], must_be_in=True)
    value, errors = field.clean(["a"])
    assert value == ["a"]
    assert errors == []

    value, errors = field.clean(["x"])
    assert value is None
    assert errors[0].code == "InList"


def test_list_field_membership_requires_not_in_list():
    field = List(listvalues=["a", "b"], must_be_in=False)
    value, errors = field.clean(["x"])
    assert value == ["x"]
    assert errors == []

    value, errors = field.clean(["a"])
    assert value is None
    assert errors[0].code == "NoInList"


def test_inlist_validator_can_run_in_not_in_mode():
    validator = InList(["a", "b"], should_be_in=False)
    assert validator("x") is None
    assert validator("a").code == "NoInList"
