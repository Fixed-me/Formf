# field.py
from Formf.Core.errors import ValidationError
from Formf.Core.schema import Schema

class Field:
    def __init__(self, *, required: bool = True, requiredif = None, default=None, nullable: bool=True, blank: bool =False, validators=None):
        self.required = False if requiredif is not None or blank else required
        self.requiredif = requiredif
        self.default = default
        self.nullable = nullable
        self.blank = blank
        self.validators = validators or []
        self.name = None


    def _apply_default(self, value, form=None):

        # Inputs missing oder None
        if value is None:
            # Test if field is required
            required_now = self.required or (self.requiredif is not None and self._requiredif_applies(form))
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

    def _field_is_filled(self, value):
        return value not in (None, "")

    def _get_other_value(self, form, field_name):
        if form is None:
            return None
        return form.data.get(field_name)

    def _evaluate_requiredif_condition(self, condition, form):
        # backward compatible: ("other_field", True/False/<exact value>)
        if isinstance(condition, tuple) and len(condition) == 2:
            field_name, expected = condition
            other_value = self._get_other_value(form, field_name)
            if isinstance(expected, bool):
                return self._field_is_filled(other_value) == expected
            return other_value == expected

        # callable support: lambda form -> bool
        if callable(condition):
            return bool(condition(form))

        # dict support:
        # {"field": "name", "not_empty": True}
        # {"field": "status", "equals": "active"}
        # {"fields": ["a", "b"], "is_empty": True, "mode": "any|all"}
        if isinstance(condition, dict):
            fields = condition.get("fields")
            field_name = condition.get("field")

            if fields is None and field_name is not None:
                fields = [field_name]

            if not fields:
                return False

            values = [self._get_other_value(form, name) for name in fields]
            mode = condition.get("mode", "any")
            aggregator = any if mode == "any" else all

            if "equals" in condition:
                target = condition["equals"]
                return aggregator(v == target for v in values)

            if condition.get("not_empty", False):
                return aggregator(self._field_is_filled(v) for v in values)

            if condition.get("is_empty", False):
                return aggregator(not self._field_is_filled(v) for v in values)

        return False

    def _requiredif_applies(self, form=None):
        if self.requiredif is None:
            return False

        # multiple conditions: any match means this field becomes required
        if isinstance(self.requiredif, list):
            return any(self._evaluate_requiredif_condition(c, form) for c in self.requiredif)

        return self._evaluate_requiredif_condition(self.requiredif, form)

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

    def _validate_requiredif(self, value, form=None):

        if self.requiredif is not None and self._requiredif_applies(form) and value is None:
            return ValidationError(
                code="requiredif",
                message="This field is required due to requiredif condition",
                meta={"requiredif": self.requiredif}
            )
        return False

    def validate(self, value, form=None):  # Field validation
        errors = []

        for fn in (
                self._validate_required,
                self._validate_nullable,
                self._validate_blank,
        ):
            e = fn(value)
            if e:
                errors.append(e)

        e = self._validate_requiredif(value, form=form)
        if e:
            errors.append(e)

        for v in self.validators:
            e = v(value)
            if e:
                errors.append(e)

        return errors

    def clean(self, raw, form=None):

        try:
            value = self.to_python(raw)
        except ValidationError as e:
            return None, [e]   # STOP here

        value = self._apply_default(value, form=form) # Add the default option to value
        if isinstance(value, ValidationError):
            return None, [value]

        errors = self.validate(value, form=form)
        if errors:
            return None, errors

        return value, []

    def to_python(self, value):
        return value

    def to_schema(self):
        return {
            "type": self.__class__.__name__.lower(),
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
