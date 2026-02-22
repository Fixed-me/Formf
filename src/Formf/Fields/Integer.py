from Formf.Core.Field import Field
from Formf.Core.errors import ValidationError

class Integer(Field):
    def __init__(self, *, required: bool =True, requiredif= None, blank: bool=False, default=None, minvalue: int=None, maxvalue: int=None, nullable: bool=True, validators=None):
        from Formf.Validators.Min import Min
        from Formf.Validators.Max import Max

        validator = []

        if minvalue is not None:
            validator.append(Min(minvalue))
        if maxvalue is not None:
            validator.append(Max(maxvalue))

        if validators is not None:
            for v in validators:
                validator.append(v)

        super().__init__(required=required, nullable=nullable, blank=blank , requiredif=requiredif, default=default, validators=validator)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ValidationError("type", "invalid_int", value)