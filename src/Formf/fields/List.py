from Formf.Core.Field import Field
from Formf.Core.errors import ValidationError
from Formf.Core.schema import Schema

class List(Field):

    def __init__(self, *, strict: bool = False, required: bool = True, requiredif=None, blank: bool = False, nullable: bool = True, default=None, listvalues=None, must_be_in: bool = True, inlist=None, notinlist=None, item_field=None, validators=None,
    ):
        from Formf.validators import InList
        validator = []

        if listvalues is not None and (inlist is not None or notinlist is not None):
            raise ValueError("Use either listvalues/must_be_in or legacy inlist/notinlist, not both")

        membership_values = listvalues
        membership_should_be_in = must_be_in

        # backward compatibility for existing API
        if inlist not in (None, False):
            membership_values = inlist
            membership_should_be_in = True
        if notinlist not in (None, False):
            membership_values = notinlist
            membership_should_be_in = False

        if membership_values is not None:
            validator.append(InList(membership_values, should_be_in=membership_should_be_in))

        self.listvalues = membership_values
        self.must_be_in = membership_should_be_in

        if validators is not None:
            for v in validators:
                validator.append(v)

        if item_field is not None and not isinstance(item_field, (str, dict, Field)):
            raise ValueError("item_field must be str, dict, Field, or None")
        self.item_field = item_field

        # for the Field class to handel the Field validators
        super().__init__(strict=strict, required=required, requiredif=requiredif, nullable=nullable, blank=blank, default=default ,validators=validator)

    # validators would return an "actual" Error if it isn't the Correct Type
    def to_python(self, value):
        if value in (None, ""):
            return None

        # List
        if isinstance(value, list):
            return value

        if self.strict:
            raise ValidationError("type", "invalid_list", value)

        # Lenient Mode
        if isinstance(value, (tuple, set)):
            return list(value)

        raise ValidationError("type", "invalid_list", value)

    def to_schema(self):
        schema = super().to_schema()
        schema["listvalues"] = Schema.serialize_value(self.listvalues)
        schema["must_be_in"] = self.must_be_in

        if self.item_field is None:
            return schema

        if isinstance(self.item_field, Field):
            schema["item_field"] = self.item_field.to_schema()
        else:
            schema["item_field"] = Schema.serialize_value(self.item_field)
        return schema
