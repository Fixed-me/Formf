from Engine.Core.Field import Field
from Engine.Core.errors import ValidationError

class Bool(Field):

    def __init__(self, *, required: bool=True, requiredif=None, blank: bool=False, nullable: bool=True, default=None, value: bool=True, validators=None):
        from Engine.validators.Bool import Bool
        validator = []

        if bool is not None and bool in (True, False):
            validator.append(Bool(value))

        if validators is not None:
            for v in validators:
                validator.append(v)

        # for the Field class to handel the Field Validators
        super().__init__(required=required, requiredif=requiredif, nullable=nullable, blank=blank, default=default,validators=validator)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value is None or value == "":
            return None
        if not isinstance(value, bool):
            return ValidationError("type", "invalid_bool")
        return value