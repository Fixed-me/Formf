from Formf import Form
from Formf.fields import Integer, Float
from Formf.validators import Min, Max


class NumberValidatorsForm(Form):
    age = Integer(validators=[Min(18), Max(120)])
    rating = Float(validators=[Min(0.0), Max(5.0)])


form = NumberValidatorsForm({"age": 30, "rating": 4.5})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
