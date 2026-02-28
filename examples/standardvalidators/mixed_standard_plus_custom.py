from Formf import Form
from Formf.fields import String
from Formf.validators import MinLength, Pattern


class MixedRulesForm(Form):
    username = String(
        required=True,
        nullable=False,
        blank=False,
        validators=[MinLength(3), Pattern(r"^[a-z0-9_]+$")],
    )
    referral_code = String(required=False, default="none")


form = MixedRulesForm({"username": "fixed_user"})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
