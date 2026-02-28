from Formf import Form
from Formf.fields import List


class TagsForm(Form):
    tags = List(inlist=["python", "formf", "validation"])


form = TagsForm({"tags": ["python", "formf"]})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
