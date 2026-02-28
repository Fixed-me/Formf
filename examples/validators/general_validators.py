from Formf import Form
from Formf.fields import String
from Formf.validators import Equals, NotEquals, InList, NotInList, Choices, Pattern, Regex


class GeneralValidatorsForm(Form):
    status = String(validators=[Equals("active"), InList(["active", "paused"])])
    role = String(validators=[NotEquals("banned"), Choices(["admin", "editor", "user"])])
    slug = String(validators=[Pattern(r"^[a-z0-9-]+$")])
    code = String(validators=[Regex(r"^[A-Z]{3}-\\d{3}$")])
    category = String(validators=[NotInList(["deprecated", "legacy"])])


form = GeneralValidatorsForm(
    {
        "status": "active",
        "role": "admin",
        "slug": "my-project-01",
        "code": "ABC-123",
        "category": "modern",
    }
)
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
