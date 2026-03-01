from Formf import Form
from Formf.fields import List


class TagsForm(Form):
    tags = List(listvalues=["python", "formf", "validation"], must_be_in=True)


form = TagsForm({"tags": ["python", "formf"]})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
