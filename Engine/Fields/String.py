from Engine.Core.Field import Field
from Engine.Core.errors import ValidationError

class String(Field):
    def __init__(self, *, required: bool = True, requiredif = None, nullable: bool=True, blank: bool =False, minlength: int = None, maxlength: int =None, validator=None):
        from Engine.validators.MaxLength import MaxLength
        from Engine.validators.MinLength import MinLength
        validators = []

        if minlength is not None:
            validators.append(MinLength(minlength))
        if maxlength is not None:
            validators.append(MaxLength(maxlength))

        if validator is not None:
            for v in validator:
                validators.append(v)

        super().__init__(required=required, nullable=nullable, blank=blank, requiredif=requiredif, validators=validators)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value is None or value == "":
            return None
        if not isinstance(value, str):
            raise ValidationError("type", "Expected string", value)
        return value