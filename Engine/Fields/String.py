from Engine.Core.Field import Field
from Engine.Core.errors import ValidationError

class String(Field):
    def __init__(self, *, required: bool = True, requiredif =None, nullable: bool=True, blank: bool =False, default=None, minlength: int = None, maxlength: int =None, validators=None):
        from Engine.Validators.MaxLength import MaxLength
        from Engine.Validators.MinLength import MinLength
        validator = []

        if minlength is not None:
            validators.append(MinLength(minlength))
        if maxlength is not None:
            validators.append(MaxLength(maxlength))

        if validators is not None:
            for v in validators:
                validator.append(v)

        super().__init__(required=required, nullable=nullable, blank=blank, requiredif=requiredif, default=default, validators=validators)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value is None or value == "":
            return None
        if not isinstance(value, str):
            return ValidationError("type", "Expected string", value)
        return value