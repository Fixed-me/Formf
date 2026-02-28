from Formf import Form
from Formf.fields import String
from Formf.formvalidators import Equals


class RegisterForm(Form):
    password = String(minlength=8)
    password_repeat = String(minlength=8)
    form_validators = [Equals("password", "password_repeat")]


form = RegisterForm({"password": "abc12345", "password_repeat": "abc12344"})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)  # cross-field errors live in errors["__all__"]
