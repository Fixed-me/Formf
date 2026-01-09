# field.py

from Engine.Core.errors import ValidationError


class Field:
    def __init__(self, *, required: bool = True, requiredif = None, default=None, blank: bool =False, validators=None):
        self.required = False if requiredif is not None or blank else required
        self.requiredif = requiredif
        self.default = default
        self.validators = validators or []
        self.name = None
        self.blank = blank

    def to_python(self, value):
        return value

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

    #
    def clean(self, raw):

        try:
            value = self.to_python(raw)
        except ValidationError as e:
            return None, [e]   # STOP here

        errors = self.validate(value)
        if errors:
            return None, errors

        return value, []

class String(Field):
    def __init__(self, *, required: bool = True, requiredif = None, blank: bool =False, min_length: int = None, max_length: int =None, regex=None, pattern=None, choices=None):
        from Engine.Core.validators.maxLength import MaxLength
        from Engine.Core.validators.minLength import MinLength
        from Engine.Core.validators.regex import Regex
        from Engine.Core.validators.pattern import Pattern
        from Engine.Core.validators.choices import Choices
        validators = []

        if choices is not None:
            validators.append(Choices(choices))
        if pattern is not None:
            validators.append(Pattern(pattern))
        if regex is not None:
            validators.append(Regex(regex))
        if min_length is not None:
            validators.append(MinLength(min_length))
        if max_length is not None:
            validators.append(MaxLength(max_length))

        super().__init__(required=required, blank=blank, requiredif=requiredif, validators=validators)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value is None or value == "":
            return None
        if not isinstance(value, str):
            return ValidationError("type", "Expected string", value)
        return value

class Int(Field):
    def __init__(self, *, required: bool =True, requiredif = None, blank: bool=False, min: int=None, max: int=None, nullable: bool=True, equals=None, choices=None):
        from Engine.Core.validators.min_int import Min
        from Engine.Core.validators.max_int import Max
        from Engine.Core.validators.nullable import Nullable
        from Engine.Core.validators.equals import Equals
        from Engine.Core.validators.not_equals import NotEquals
        from Engine.Core.validators.choices import Choices
        validators = []


        if nullable:
            validators.append(Nullable(nullable))
        if min is not None:
            validators.append(Min(min))
        if max is not None:
            validators.append(Max(max))
        if equals is not None and equals is True:
            validators.append(Equals(equals))
        elif equals is not None and equals is False:
            validators.append(NotEquals(equals))
        if choices is not None:
            validators.append(Choices(choices))

        super().__init__(required=required, blank=blank , requiredif=requiredif, validators=validators)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ValidationError("type", "invalid_int", value)

class Float(Field):

    def __init__(self, *, required: bool=True, blank=False, min: int=None, max: int=None, nullable=True, equals=None, choices=None):
        from Engine.Core.validators.min_int import Min
        from Engine.Core.validators.max_int import Max
        from Engine.Core.validators.nullable import Nullable
        from Engine.Core.validators.equals import Equals
        from Engine.Core.validators.not_equals import NotEquals
        from Engine.Core.validators.choices import Choices
        validators = []

        if nullable is not True:
            validators.append(Nullable(nullable))
        if min is not None:
            validators.append(Min(min))
        if max is not None:
            validators.append(Max(max))
        if equals is not None and equals is True:
            validators.append(Equals(equals))
        if equals is not None and equals is False:
            validators.append(NotEquals(equals))
        if choices is not None:
            validators.append(Choices(choices))

        # for the Field class to handel the Field Validators
        super().__init__(required=required, blank=blank ,validators=validators)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValidationError("type", "invalid_float")

class Bool(Field):

    def __init__(self, *, required: bool=True, blank: bool=False, bool_value=True):
        from Engine.Core.validators.bool import Bool
        validators = []

        if bool is not None and bool in (True, False):
            validators.append(Bool(bool_value))

        # for the Field class to handel the Field Validators
        super().__init__(required=required, blank=blank ,validators=validators)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value is None or value == "":
            return None
        if not isinstance(value, bool):
            raise ValidationError("type", "invalid_bool")
        return value
    
class Email(String):
    def __init__(self, *, required: bool=True, blank: bool=False, regex=None):
        from Engine.Core.validators.email import Email
        from Engine.Core.validators.regex import Regex
        validators = []
        
        if regex is not None:
            validators.append(Regex(regex))
        validators.append(Email())

        # for the Field class to handel the Field Validators
        super().__init__(required=required, blank=blank)

class List(Field):

    def __init__(self, *, required: bool=True, blank: bool=False, list=None, inlist: bool=True):
        from Engine.Core.validators.inList import InList
        from Engine.Core.validators.notInList import NotInList
        validators = []

        if list is not None and inlist is True:
            validators.append(InList(list, inlist))
        elif list is not None and inlist is False:
            validators.append(NotInList(list, inlist))

        # for the Field class to handel the Field Validators
        super().__init__(required=required, blank=blank ,validators=validators)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value is None or value == "":
            return None
        try:
            return list(value)
        except (ValueError, TypeError):
            raise ValidationError("type", "invalid_List", value)

class Url(String):

    def __init__(self, *, required: bool=True, blank: bool=False, regex=None):
        from Engine.Core.validators.url import URL
        validators = []

        if regex is not None:
            validators.append(URL(regex))

        # for the Field class to handel the Field Validators
        super().__init__(required=required, blank=blank)

class Date(Field):

    def __init__(self, *, required: bool=True, blank: bool=False, date_format=None, before=None, after=None):
        from Engine.Core.validators.date import Date
        from Engine.Core.validators.before_datetime import Before
        from Engine.Core.validators.after_datetime import After

        validators = []

        if date_format is not None:
            validators.append(Date(date_format))
        if before is not None and date_format is not None:
            validators.append(Before(before, date_format))
        if after is not None and date_format is not None:
            validators.append(After(after, date_format))

        # for the Field class to handel the Field Validators
        super().__init__(required=required, blank=blank , validators=validators)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):

        if value is None or value == "":
            return None
        if not isinstance(value, str):
            return ValidationError("type", "invalid_format", value)
        return value