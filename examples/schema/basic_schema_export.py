import json

from Formf import Form
from Formf.fields import String, Integer


class UserForm(Form):
    username = String(minlength=3, maxlength=20)
    age = Integer(required=False, minvalue=18)


schema = UserForm({}).to_schema()
print(json.dumps(schema, indent=2))
