from email.policy import default

from Engine.Core.Field import Field
from Engine.Core.errors import ValidationError

class Date(Field):

    def __init__(self, *, required: bool=True, requiredif=None, blank: bool=False, nullable: bool=None, default=None, dateformat=None, before=None, after=None, validators=None):
        from Engine.validators import Dateformat
        from Engine.validators.BeforeDate import Before
        from Engine.validators.AfterDate import After

        validator = []

        if dateformat is not None:
            validator.append(Dateformat(dateformat))
        if before is not None:
            validator.append(Before(before, dateformat))
        if after is not None:
            validator.append(After(after, dateformat))

        if validators is not None:
            for v in validators:
                validator.append(v)

        # for the Field class to handel the Field Validators
        super().__init__(required=required, requiredif=requiredif, nullable=nullable, blank=blank, default=default , validators=validator)

    # Validators would return an "actual" Error if it isn't the Correct Type
    from datetime import datetime

    def to_python(self, value):
        from datetime import datetime

        if value is None or value == "":
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            # Possible Date formats
            formats = [
                "%Y-%m-%d",
                "%d-%m-%Y",
                "%m-%d-%Y",
                "%Y/%m/%d",
                "%d/%m/%Y",
                "%m/%d/%Y",
            ]
            for token in sorted(formats, key=len, reverse=True):
                try:
                    datetime.strptime(value, token)
                    return value
                except ValueError:
                    raise ValidationError("type", "invalid_date", value)
        raise ValidationError("type", "invalid_date", value)
