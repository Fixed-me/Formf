from Formf import Form
from Formf.fields import String, Integer


class BasicStandardOptionsForm(Form):
    username = String(required=True)
    nickname = String(required=False, blank=True)
    bio = String(required=False, nullable=True)
    retries = Integer(required=False, default=3)


form = BasicStandardOptionsForm({"username": "fixed"})
print(form.is_valid())
print(form.cleaned_data)  # includes default retries=3
print(form.errors)
