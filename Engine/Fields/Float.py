from Engine.Core.Field import Field
from Engine.Core.errors import ValidationError

class Float(Field):

    def __init__(self, *, required: bool=True, requiredif=None, nullable: bool=True, blank: bool=False, default=None, maxvalue: float=None, minvalue: float=None, validators=None):
        from Engine.Validators.Max import Max
        from Engine.Validators.Min import Min
        validator = []

        if Max is not None:
            validator.append(Max(maxvalue))
        if Min is not None:
            validator.append(Min(minvalue))

        if validators is not None:
            for v in validators:
                validator.append(v)

        # for the Field class to handel the Field Validators
        super().__init__(required=required, requiredif=requiredif, blank=blank, nullable=nullable, default=default ,validators=validators)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value is None or value == "":
            return None
        if not isinstance(value, float):
            return ValidationError("type", "Expected Float", value)
        return value
