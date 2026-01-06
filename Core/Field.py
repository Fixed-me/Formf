# fields.py

from Core.errors import ValidationError

class Field:
    def __init__(self, *, required=False, default=None, validators=None):
        self.required = required
        self.default = default
        self.validators = validators or []
        self.name = None

    def to_python(self, value):
        return value

    def _validate_required(self, value):
        if self.required and (value is None or value == ""):
            return ValidationError(
                code="required",
                message="This field is required"
            )
        return None

    def validate(self, value):
        errors = []

        # required check
        err = self._validate_required(value)
        if err:
            return [err]

        for v in self.validators:
            e = v(value)
            if e:
                errors.append(e)

        return errors

    def clean(self, raw):
        if raw is None:
            if self.required:
                return None, [ValidationError("required")]
            return self.default, []

        try:
            value = self.to_python(raw)
        except ValidationError as e:
            return None, [e]   # STOP here

        errors = self.validate(value)
        if errors:
            return None, errors

        return value, []

class String(Field):
    def __init__(self, *, required=False, min_length=None, max_length=None, regex=None):
        validators = []
        from Core.validators.MaxLength import MaxLength
        from Core.validators.MinLength import MinLength
        from Core.validators.Regex import Regex
        
        if regex is not None:
            validators.append(Regex(regex))
        if min_length is not None:
            validators.append(MinLength(min_length))
        if max_length is not None:
            validators.append(MaxLength(max_length))

        super().__init__(required=required, validators=validators)

    def to_python(self, value):
        if value is None:
            return None
        if not isinstance(value, str):
            return ValidationError("type", "Expected string")
        return value

class Int(Field):
    def __init__(self, *, required=False, min=None, max=None, nullable=True):
        validators = []
        from Core.validators.Min import Min
        from Core.validators.Max import Max
        from Core.validators.Nullable import Nullable

        if nullable is not True:
            validators.append(Nullable(nullable))
        if min is not None:
            validators.append(Min(min))
        if max is not None:
            validators.append(Max(max))

        super().__init__(required=required, validators=validators)

    def to_python(self, value):
        if value is None or value == "":
            return None
        try:
            return int(value)
        except:
            raise ValidationError("type", "invalid_int")

class Float(Field):
    def __init__(self, *, required=False, min=None, max=None, nullable=True):
        validators = []
        from Core.validators.Min import Min
        from Core.validators.Max import Max
        from Core.validators.Nullable import Nullable

        if nullable is not True:
            validators.append(Nullable(nullable))
        if min is not None:
            validators.append(Min(min))
        if max is not None:
            validators.append(Max(max))

        super().__init__(required=required, validators=validators)

    def to_python(self, value):
        if value is None or value == "":
            return None
        try:
            return float(value)
        except ValidationError:
            raise ValidationError("type", "invalid_float")

class Email(String):
    def __init__(self, *, required=False, regex=None):
        from Core.validators.Email import Email
        from Core.validators.Regex import Regex
        validators = []
        
        if regex is not None:
            validators.append(Regex(regex))
        validators.append(Email())
        
        super().__init__(required=required)

class list(Field):

    def __init__(self, *, required=False, list=None, inList=True):
        validators = []
        from Core.validators.InList import InList
        from Core.validators.NotInList import NotInList
        
        if list is not None and inList is True:
            validators.append(InList(list, inList))
        elif list is not None and inList is False:
            validators.append(NotInList(list, inList))
        super().__init__(required=required)