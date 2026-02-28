from Formf import Form
from Formf.fields import String
from Formf.validators import MinLength, MaxLength, Lowercase, Uppercase, Email, Url


class StringValidatorsForm(Form):
    password = String(validators=[MinLength(8), MaxLength(64)])
    username = String(validators=[Lowercase()])
    country_code = String(validators=[Uppercase()])
    email = String(validators=[Email()])
    website = String(validators=[Url()])


form = StringValidatorsForm(
    {
        "password": "super-secure-password",
        "username": "fixed",
        "country_code": "DE",
        "email": "fixed@example.com",
        "website": "https://example.com",
    }
)
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
