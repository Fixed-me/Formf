# fields.py

from Core.errors import ValidationError

class Field:
    def __init__(self, *, required=True, default=None, blank=False, validators=None):
        self.required = required
        self.default = default
        self.validators = validators or []
        self.name = None
        self.blank = blank

    def to_python(self, value):
        return value

    def _validate_required(self, value):
        if self.required and (value is None):
            return ValidationError(
                "required",
                "This field is required"
            )
        return None
    
    def _validate_required(self, value):
        if self.blank and (value == ""):
            return ValidationError(
                "blank",
                "This Field may not be blank"
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
    def __init__(self, *, required=True, min_length=None, max_length=None, regex=None):
        validators = []
        from Core.validators.maxLength import MaxLength
        from Core.validators.minLength import MinLength
        from Core.validators.regex import Regex
        
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
            return ValidationError("type", "Expected string", value)
        return value

class Int(Field):
    def __init__(self, *, required=True, min=None, max=None, nullable=True):
        from Core.validators.min import Min
        from Core.validators.max import Max
        from Core.validators.nullable import Nullable
        validators = []

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
        except (ValueError, TypeError):
            raise ValidationError("type", "invalid_int", value)

class Float(Field):

    def __init__(self, *, required=True, min=None, max=None, nullable=True):
        from Core.validators.min import Min
        from Core.validators.max import Max
        from Core.validators.nullable import Nullable
        validators = []

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
        except (ValueError, TypeError):
            raise ValidationError("type", "invalid_float")

class Bool(Field):

    def __init__(self, *, required=True, bool=True):
        from Core.validators.bool import Bool
        validators = []

        if bool is not None and bool in (True, False):
            validators.append(Bool(bool))

        super().__init__(required=required, validators=validators)

    def to_python(self, value):
        if value is None or value == "":
            return None
        if not isinstance(value, bool):
            raise ValidationError("type", "invalid_bool")
        return value
    
class Email(String):
    def __init__(self, *, required=True, regex=None):
        from Core.validators.email import Email
        from Core.validators.regex import Regex
        validators = []
        
        if regex is not None:
            validators.append(Regex(regex))
        validators.append(Email())
        
        super().__init__(required=required)

class List(Field):

    def __init__(self, *, required=True, list=None, inList=True):
        from Core.validators.inList import InList
        from Core.validators.notInList import NotInList
        validators = []

        if list is not None and inList is True:
            validators.append(InList(list, inList))
        elif list is not None and inList is False:
            validators.append(NotInList(list, inList))
        super().__init__(required=required, validators=validators)
    
    def to_python(self, value):
        if value is None or value == "":
            return None
        try:
            return List(value)
        except (ValueError, TypeError):
            raise ValidationError("type", "invalid_List", value)

class Url(String):

    def __init__(self, *, required=True):
        from Core.validators.url import URL
        validators = []

        validators.append(URL())

        super().__init__(required=required)

class Date(String):

    def __init__(Self, *, required=True, format=None, before=None, after=None):
        from Core.validators.date import Date
        from Core.validators.before import Before
        from Core.validators.after import After
        
        validators = []

        if format is not None:
            validators.append(Date(format))
        if before is not None:
            validators.append(Before(before))
        if after is not None:
            validators.append(After(after))
        
        super().__init__(required=required)
    
    def to_python(self, value):
        from datetime import date
        if value is None or value == "":
            return None
        if not isinstance(value, date):
            return ValidationError("type", "invalid_format", value)
        return value