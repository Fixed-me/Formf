from Formf import Form
from Formf.fields import Date, Bool
from Formf.validators import After

class Registerform(Form):
    field1 = Date(validators=[After(after="1010-08-19")])
    field2 = Bool(value=False)

data = {
    "field1": "1010-08-19",
    "field2": True
}

form = Registerform(data)

print(form.is_valid())
print(form.errors())