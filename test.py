from Formf import Form
from Formf.fields import Date, Bool
from Formf.validators import After

class Registerform(Form):
    field1 = Date(validators=[After("1010-08-19")])
    field2 = Bool()

data = {
    "field1": "1010-08-18",
    "field2": False
}

form = Registerform(data)

print(form.is_valid())
print(form.errors)