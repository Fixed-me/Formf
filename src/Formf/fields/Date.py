from Formf.Core.Field import Field
from Formf.Core.errors import ValidationError

class Date(Field):

    def __init__(self, *, strict=None, required: bool=True, requiredif=None, blank: bool=False, nullable: bool=None, default=None, dateformat=None, before=None, after=None, validators=None):
        from Formf.validators import Dateformat
        from Formf.validators.BeforeDate import Before
        from Formf.validators.AfterDate import After

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

        self.dateformat = dateformat
        self.before = before
        self.after = after

        # for the Field class to handel the Field validators
        super().__init__(strict=strict, required=required, requiredif=requiredif, nullable=nullable, blank=blank, default=default , validators=validator)

    # validators would return an "actual" Error if it isn't the Correct Type

    def to_python(self, value):
        from datetime import datetime

        if value in (None, ""):
            return None

        if isinstance(value, datetime):
            return value

        if not isinstance(value, str):
            raise ValidationError("type", "invalid_date", value)

        value = value.strip()

        if self.strict:
            try:
                return datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValidationError("type", "invalid_date", value)

        # lenient mode
        formats = [
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        raise ValidationError("type", "invalid_date", value)

    def to_schema(self):
        schema = super().to_schema()
        schema["dateformat"] = self.dateformat
        schema["before"] = self.before
        schema["after"] = self.after
        return schema
