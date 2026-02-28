from Formf import Form
from Formf.fields import String


class RequiredIfDictAndListForm(Form):
    role = String(required=False)
    plan = String(required=False)
    first_name = String(required=False)
    last_name = String(required=False)
    status = String(required=False)

    # required if any of role/plan equals "pro"
    reason = String(requiredif={"fields": ["role", "plan"], "equals": "pro", "mode": "any"})

    # required if all listed fields are not empty
    nickname = String(requiredif={"fields": ["first_name", "last_name"], "not_empty": True, "mode": "all"})

    # required if status == "approved" OR role == "admin"
    support_note = String(
        requiredif=[
            {"field": "status", "equals": "approved"},
            {"field": "role", "equals": "admin"},
        ]
    )


form = RequiredIfDictAndListForm(
    {
        "role": "pro",
        "plan": "basic",
        "first_name": "Noah",
        "last_name": "Fischer",
        "status": "pending",
    }
)
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
