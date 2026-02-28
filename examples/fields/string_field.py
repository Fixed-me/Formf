from Formf import Form
from Formf.fields import String


class ProfileForm(Form):
    username = String(minlength=3, maxlength=20)


form = ProfileForm({"username": "noah"})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
