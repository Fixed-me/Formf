# user_code.py
from Core.Form import Form
from Core.Field import String, Int, Email

class RegisterForm(Form):
    email = Email()
    password = String(min_length=8, max_length=11)
    age = Int(min=18, max=20)

good_data = {
    "email": "1123",
    "password": "supersecret",
    "age": "1"
}

form = RegisterForm(good_data)

print(form.is_valid())
print(form.errors)