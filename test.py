from Formf import Form, Field
from Formf.Core import ValidationError
from Formf.validators import Min

data = {
    "field2": 9
}

class Integer(Field):

    def to_python(self, value):
        if value in (None, ""):
            return None

        if not type(value) is int:
            raise ValidationError("type_integer", meta={"integer": value})

        return value

class Registerform(Form):
    field2 = Integer()

form = Registerform(data)

print(form.is_valid())
print(form.errors())