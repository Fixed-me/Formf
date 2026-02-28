from Formf import Form
from Formf.fields import Bool
from Formf.validators import Bool as BoolValidator


class BoolValidatorForm(Form):
    accepted_terms = Bool(validators=[BoolValidator(True)])


form = BoolValidatorForm({"accepted_terms": True})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
