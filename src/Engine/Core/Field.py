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

    def _apply_default(self, value):

        # Inputs missing oder None
        if value is None:
            # Test if field is required
            required_now = self.required or (self.requiredif is not None and self._requiredif_applies())
            if required_now:
                if self.default is None:
                    return ValidationError(
                        "default",
                        "no default value provided",
                        meta={"Default": self.default}
                    )
            # Fallback default
            value = self.default

        return value

    def _requiredif_applies(self):
        if self.requiredif is None:
            return False

        other, expected = self.requiredif
        is_filled = other not in (None, "")
        return (is_filled and expected) or (not is_filled and not expected)

    def _validate_required(self, value):
        if self.required and (value is None):
            return ValidationError(
                "required",
                "This field is required",
                meta={"Required": self.required}

            )

        return False

    def _validate_nullable(self, value):

        if not self.nullable and (value is None):
            return ValidationError(
                code="nullable",
                message="This Field may not be empty",
                meta={"Required": self.required}
            )
        return False


    
    def _validate_blank(self, value):
        if self.blank and isinstance(value, str) and value == "":
            return ValidationError(
                "blank",
                "This Field may not be blank"
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

    def validate(self, value):  # Field validation
        errors = []

        for fn in (
                self._validate_required,
                self._validate_nullable,
                self._validate_blank,
        ):
            e = fn(value)
            if e:
                errors.append(e)

        e = self._validate_requiredif(value)
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

        value = self._apply_default(value) # Add the default option to value
        if isinstance(value, ValidationError):
            return None, [value]

        errors = self.validate(value)
        if errors:
            return None, errors

        return value, []

    def to_python(self, value):
        return value