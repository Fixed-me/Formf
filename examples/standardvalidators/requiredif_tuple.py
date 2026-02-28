from Formf import Form
from Formf.fields import String


class RequiredIfTupleForm(Form):
    # required if status is not empty
    status_reason = String(requiredif=("status", True))

    # required if middle_name is empty
    suffix = String(requiredif=("middle_name", False))

    # required if status == "approved"
    approval_note = String(requiredif=("status", "approved"))


form = RequiredIfTupleForm({"status": "approved", "middle_name": ""})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
