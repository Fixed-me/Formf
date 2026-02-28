from Formf import Form
from Formf.fields import String, Integer


class RequiredIfCallableForm(Form):
    name = String(required=False)
    age = Integer(requiredif=lambda form: form.data.get("name") == "Alice")


form = RequiredIfCallableForm({"name": "Alice"})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
