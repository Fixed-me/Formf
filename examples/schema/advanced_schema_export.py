import json

from Formf import Form
from Formf.fields import String
from Formf.formvalidators import Equals, BeforeDate


class RegisterForm(Form):
    status = String(required=False)
    email = String(requiredif=("status", "approved"))
    support_note = String(
        requiredif=[
            {"field": "status", "equals": "approved"},
            lambda form: form.data.get("status") == "urgent",
        ]
    )

    password = String(minlength=8)
    password_repeat = String(minlength=8)
    start_date = String()
    end_date = String()

    form_validators = [
        Equals("password", "password_repeat"),
        BeforeDate("start_date", "end_date"),
    ]


schema = RegisterForm({}).to_schema()
print(json.dumps(schema, indent=2))
