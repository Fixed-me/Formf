# user_code.py
from Engine.Core.Form import Form
from Engine.Core.Field import String, Int

class RegisterForm(Form):
    Str = String()
    password = Int(requiredif=(Str, True))

data = {
    "Str": "aaaa",
    "password": ""
}


form = RegisterForm(data)

print(form.is_valid())
print(form.errors)