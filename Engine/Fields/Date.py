from Engine.Core.Field import Field
from Engine.Core.errors import ValidationError

class Date(Field):

    def __init__(self, *, required: bool=True, requiredif=None, blank: bool=False, nullable: bool=None, dateformat=None, before=None, after=None, validators=None):
        from Engine.validators import Dateformat
        from Engine.validators.BeforeDatetime import Before
        from Engine.validators.AfterDatetime import After

        validator = []

        if dateformat is not None:
            validator.append(Dateformat(dateformat))
        if before is not None:
            validator.append(Before(before, dateformat))
        if after is not None:
            validator.append(After(after, dateformat))

        for v in validators:
            validator.append(v)

        # for the Field class to handel the Field Validators
        super().__init__(required=required, requiredif=requiredif, nullable=nullable, blank=blank , validators=validator)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        from datetime import datetime
        if value is None or value == "":
            return None
        if not isinstance(value, datetime):
            raise ValidationError("type", "invalid_dateformat", value)
        return value