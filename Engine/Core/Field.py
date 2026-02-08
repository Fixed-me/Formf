# field.py
from Engine.Core.errors import ValidationError

class Field:
    def __init__(self, *, required: bool = True, requiredif = None, default=None, nullable: bool=True, blank: bool =False, validators=None):
        self.required = False if requiredif is not None or blank else required
        self.requiredif = requiredif
        self.default = default
        self.nullable = nullable
        self.validators = validators or []
        self.name = None
        self.blank = blank

    def to_python(self, value):
        return value

    def _validate_nullable(self, value):

        if not self.nullable and (value == 0 or value == ""):
            return ValidationError(
                code="nullable",
                message="This Field may not be empty",
                meta={"Required": self.required}
            )
        return False

    def _validate_requiredif(self, value):

        if self.requiredif is not None:
            other, expected = self.requiredif

            if expected and other in (None, ""):

                if value is None:
                    return ValidationError(
                        code="requiredif",
                        message="This field is required if another field is provided",
                        meta={"Required": expected}
                    )
        return False

    def _validate_required(self, value):
        if self.required and (value is None):
            return ValidationError(
                "required",
                "This field is required",
                meta={"Required": self.required}

            )

        return False
    
    def _validate_blank(self, value):
        if self.blank and (value == ""):
            return ValidationError(
                "blank",
                "This Field may not be blank"
            )
        return False

    def validate(self, value): # Field validation
        errors = []

        for fn in (
                self._validate_required,
                self._validate_blank,
                self._validate_requiredif,
        ):
            e = fn(value)
            if e:
                errors.append(e)

        for v in self.validators:
            e = v(value)
            if e:
                errors.append(e)

        return errors

    def clean(self, raw):

        try:
            value = self.to_python(raw)
        except ValidationError as e:
            return None, [e]   # STOP here

        errors = self.validate(value)
        if errors:
            return None, errors

        return value, []