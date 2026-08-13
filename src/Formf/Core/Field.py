# field.py
from Formf.Core.errors import ValidationError
from Formf.Core.schema import Schema
from Formf.Core.helper import run_validator
from Formf.validators.Required import Required
from Formf.validators.Nullable import Nullable
from Formf.validators.Blank import Blank
from Formf.validators.RequiredIf import RequiredIf

class Field:

    validators = []

    def __init__(self, *, strict: bool=False, required: bool = True, requiredif = None, default=None, nullable: bool=True, blank: bool =False, validators=None):
        self.required = False if requiredif is not None or blank else required
        self.requiredif = requiredif
        self.default = default
        self.nullable = nullable
        self.blank = blank
        self.name = None
        self.strict = strict

        self.validators = [
            Required(self.required),
            Nullable(self.nullable),
            Blank(self.blank),
            RequiredIf(self.requiredif)
        ]

        self.validators.extend(self.__class__.validators)

        if validators:
            self.validators.extend(validators)

    def _apply_default(self, value, form=None):

        # Inputs missing or None
        if value is None:
            # Test if field is required
            required_now = self.required or (self.requiredif is not None and RequiredIf._requiredif_applies(form))
            if required_now:
                if self.default is None:
                    return ValidationError(
                        "default",
                        meta={"Default": self.default},
                        value={"Input": value}
                    )
            # Fallback default
            value = self.default

        return value

    async def validate(self, value):  # Field validation
        errors = []

        for validator in self.validators:
            error = await run_validator(validator, value)
            if error:
                errors.append(error)

        return errors

    async def clean(self, raw, form=None):

        try:
            value = self.to_python(raw)
        except ValidationError as e:
            return None, [e]   # STOP here

        value = self._apply_default(value, form=form) # Add the default option to value
        if isinstance(value, ValidationError):
            return None, [value]

        errors = await self.validate(value)
        if errors:
            return None, errors

        return value, []

    def to_python(self, value):
        return value

    def to_schema(self):
        return {
            "type": self.__class__.__name__.lower(),
            "strict": self.strict,
            "required": self.required,
            "requiredif": Schema.serialize_requiredif(self.requiredif),
            "nullable": self.nullable,
            "blank": self.blank,
            "default": Schema.serialize_value(self.default),
            "validators": [
                Schema.serialize_validator(v)
                for v in self.validators
            ],
        }
