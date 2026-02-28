from Formf import Form
from Formf.fields import Date
from Formf.validators import Before, After, Dateformat


class DateValidatorsForm(Form):
    launch_date = Date(validators=[Dateformat("%Y-%m-%d"), After("2020-01-01", "%Y-%m-%d")])
    freeze_date = Date(validators=[Dateformat("%Y-%m-%d"), Before("2030-01-01", "%Y-%m-%d")])


form = DateValidatorsForm({"launch_date": "2025-01-01", "freeze_date": "2029-12-31"})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
