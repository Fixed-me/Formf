from Formf import Form
from Formf.fields import String
from Formf.formvalidators import Equals, BeforeDate


class CheckoutForm(Form):
    password = String(minlength=8)
    password_repeat = String(minlength=8)
    shipping_date = String()
    delivery_date = String()

    form_validators = [
        Equals("password", "password_repeat"),
        BeforeDate("shipping_date", "delivery_date"),
    ]


form = CheckoutForm(
    {
        "password": "abc12345",
        "password_repeat": "abc12345",
        "shipping_date": "10.01.2020",
        "delivery_date": "12.01.2020",
    }
)
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
