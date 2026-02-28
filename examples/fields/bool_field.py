from Formf import Form
from Formf.fields import Bool


class TermsForm(Form):
    accepted_terms = Bool(value=True)


form = TermsForm({"accepted_terms": True})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
