# user_code.py
from Engine import String, MinLength, Form


class RegisterForm(Form):
    Str = String(validator=[MinLength(3)])

data = {
    "Str": "aa",
    "password": ""
}

form = RegisterForm(data)

print(form.is_valid())
print(form.errors)