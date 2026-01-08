# user_code.py
from Core.Form import Form
from Core.Field import Date, Bool

class RegisterForm(Form):
    email = Date(format="DD-MM-YYYY")
    password = Bool(bool=True)

data = {
    "email": "19-08-2026",
    "password": True
}

form = RegisterForm(data)

print(form.is_valid())
print(form.errors)