from Formf.Core.Field import Field
from Formf.Core.errors import ValidationError

class Float(Field):

    def __init__(self, *, strict: bool=False, required: bool=True, requiredif=None, nullable: bool=True, blank: bool=False, default=None, maxvalue: float=None, minvalue: float=None, validators=None):
        from Formf.validators.Max import Max
        from Formf.validators.Min import Min
        validator = []

        if Max is not None:
            validator.append(Max(maxvalue))
        if Min is not None:
            validator.append(Min(minvalue))

        if validators is not None:
            for v in validators:
                validator.append(v)

        self.minvalue = minvalue
        self.maxvalue = maxvalue

        # for the Field class to handel the Field validators
        super().__init__(strict=strict, required=required, requiredif=requiredif, blank=blank, nullable=nullable, default=default ,validators=validator)

    # validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value in (None, ""):
            return None

        # float
        if isinstance(value, float):
            return value

        if self.strict:
            raise ValidationError("type", "invalid_Float", value)

        # Lenient Mode
        if isinstance(value, int):
            return float(value)

        if isinstance(value, str):
            try:
                return float(value.strip())
            except ValueError:
                pass

        raise ValidationError("type", "invalid_Float", value)

    def to_schema(self):
        schema = super().to_schema()
        schema["minvalue"] = self.minvalue
        schema["maxvalue"] = self.maxvalue
        return schema
