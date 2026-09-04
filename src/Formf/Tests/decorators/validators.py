import pytest

from Formf.decorators.validators import ValidatorDefinition
from Formf.decorators import validators

def test_validator_definition():
    def my_validator(value):
        return True

    definition = ValidatorDefinition("username", my_validator)

    assert definition.field_name == "username"
    assert definition.name == "my_validator"
    assert definition.function is my_validator

def test_validators_decorator():
    def my_validator(value):
        return True

    definition = validators("username")(my_validator)

    assert definition.field_name == "username"
    assert definition.function is my_validator