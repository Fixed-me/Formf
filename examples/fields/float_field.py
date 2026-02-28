from Formf import Form
from Formf.fields import Float


class PriceForm(Form):
    amount = Float(minvalue=1.0, maxvalue=9999.99)


form = PriceForm({"amount": 24.5})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
