from Engine.Core.Field import Field
from Engine.Core.errors import ValidationError

class List(Field):

    def __init__(self, *, required: bool=True, requiredif=None, blank: bool=False, nullable: bool=True, default=None, inlist: list=True, notinlist: list=False, validators=None):
        from Engine.Validators import InList
        from Engine.Validators import NotInList
        validator = []

        if inlist:
            validator.append(InList(inlist))
        if notinlist:
            validator.append(NotInList(notinlist))

        if validators is not None:
            for v in validators:
                validator.append(v)

        # for the Field class to handel the Field Validators
        super().__init__(required=required, requiredif=requiredif, nullable=nullable, blank=blank, default=default ,validators=validators)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value is None or value == "":
            return None
        try:
            return list(value)
        except (ValueError, TypeError):
            raise ValidationError("type", "invalid_List", value)
