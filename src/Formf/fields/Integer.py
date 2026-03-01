from Formf.Core.Field import Field
from Formf.Core.errors import ValidationError

class Integer(Field):
    def __init__(self, *, strict: bool=False, required: bool =True, requiredif= None, blank: bool=False, default=None, minvalue: int=None, maxvalue: int=None, nullable: bool=True, validators=None):
        from Formf.validators.Min import Min
        from Formf.validators.Max import Max

        validator = []

        if minvalue is not None:
            validator.append(Min(minvalue))
        if maxvalue is not None:
            validator.append(Max(maxvalue))

        if validators is not None:
            for v in validators:
                validator.append(v)

        self.minvalue = minvalue
        self.maxvalue = maxvalue

        super().__init__(strict=strict, required=required, nullable=nullable, blank=blank , requiredif=requiredif, default=default, validators=validator)

    # validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value in (None, ""):
            return None

        # Int
        if isinstance(value, int):
            return value

        if self.strict:
            raise ValidationError("type", "invalid_integer", value)

        # Lenient Mode
        if isinstance(value, float):
            return int(value)

        if isinstance(value, str):
            try:
                return int(value.strip())
            except ValueError:
                pass

        raise ValidationError("type", "invalid_integer", value)

    def to_schema(self):
        schema = super().to_schema()
        schema["minvalue"] = self.minvalue
        schema["maxvalue"] = self.maxvalue
        return schema
