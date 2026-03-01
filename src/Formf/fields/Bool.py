from Formf.Core.Field import Field
from Formf.Core.errors import ValidationError

class Bool(Field):

    def __init__(self, *, strict=None ,required: bool=True, requiredif=None, blank: bool=False, nullable: bool=True, default=None, value: bool=True, validators=None):
        from Formf.validators.Bool import Bool
        validator = []

        if value is not None and value in (True, False):
            validator.append(Bool(value))

        if validators is not None:
            for v in validators:
                validator.append(v)

        self.value = value

        # for the Field class to handel the Field validators
        super().__init__(strict=strict, required=required, requiredif=requiredif, nullable=nullable, blank=blank, default=default, validators=validator)

    # validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value is None or value == "":
            return None
        if not isinstance(value, bool):
            raise ValidationError("type", "invalid_bool")

        if not self.strict:
            if isinstance(value, str):
                v = value.lower()
                if v in ("true", "1", "yes"):
                    return True
                if v in ("false", "0", "no"):
                    return False

        if isinstance(value, int):
            return bool(value)

        return value

    def to_schema(self):
        schema = super().to_schema()
        schema["value"] = self.value
        return schema
