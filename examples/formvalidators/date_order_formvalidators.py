from Formf import Form
from Formf.fields import String
from Formf.formvalidators import BeforeDate, AfterDate


class DateRangeForm(Form):
    start_date = String()
    end_date = String()

    # both rules are shown for demonstration.
    # in real usage you typically keep only one of them.
    form_validators = [
        BeforeDate("start_date", "end_date"),
        AfterDate("end_date", "start_date"),
    ]


form = DateRangeForm({"start_date": "09.01.2020", "end_date": "10.01.2020"})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
