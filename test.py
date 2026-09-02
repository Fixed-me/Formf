from Formf import Form, Field
from Formf.Core import ValidationError
from Formf.fields import Integer
from Formf.decorators import validators

data = {
    "field2": 9
}

class Registerform(Form):
    field2 = Integer()

    @validators("field2")
    def validator(self, value):
        if value > 0:
            return ValidationError(code="greater than", message="Field must be greater than 0", value=value)

        return value

form = Registerform(data)

print(form.is_valid())
print(form.errors())