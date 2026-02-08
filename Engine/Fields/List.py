from Engine.Core.Field import Field
from Engine.Core.errors import ValidationError

class List(Field):

    def __init__(self, *, required: bool=True, requiredif=None, blank: bool=False, nullable: bool=True, inlist: list=True, notinlist: list=False, validators=None):
        from Engine.validators import InList
        from Engine.validators import NotInList
        validator = []

        if inlist:
            validator.append(InList(inlist))
        if notinlist:
            validator.append(NotInList(notinlist))

        for v in validators:
            validator.append(v)

        # for the Field class to handel the Field Validators
        super().__init__(required=required, requiredif=requiredif, nullable=nullable,blank=blank ,validators=validators)

    # Validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value is None or value == "":
            return None
        try:
            return list(value)
        except (ValueError, TypeError):
            raise ValidationError("type", "invalid_List", value)
