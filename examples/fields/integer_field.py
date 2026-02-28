from Formf import Form
from Formf.fields import Integer


class AgeForm(Form):
    age = Integer(minvalue=18, maxvalue=120)


form = AgeForm({"age": "21"})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
