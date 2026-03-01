from Formf.Core.Field import Field
from Formf.Core.errors import ValidationError

class String(Field):
    def __init__(self, *, strict: bool=False, required: bool = True, requiredif =None, nullable: bool=True, blank: bool =False, default=None, minlength: int = None, maxlength: int =None, validators=None):
        from Formf.validators.MaxLength import MaxLength
        from Formf.validators.MinLength import MinLength
        validator = []

        if minlength is not None:
            validator.append(MinLength(minlength))
        if maxlength is not None:
            validator.append(MaxLength(maxlength))

        if validators is not None:
            for v in validators:
                validator.append(v)

        self.minlength = minlength
        self.maxlength = maxlength

        super().__init__(strict=strict, required=required, nullable=nullable, blank=blank, requiredif=requiredif, default=default, validators=validator)

    # validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value in (None, ""):
            return None

        # Str
        if isinstance(value, str):
            return value

        if self.strict:
            raise ValidationError("type", "Expected string", value)

        # Lenient Mode
        try:
            return str(value)
        except Exception:
            raise ValidationError("type", "Expected string", value)

    def to_schema(self):
        schema = super().to_schema()
        schema["minlength"] = self.minlength
        schema["maxlength"] = self.maxlength
        return schema
