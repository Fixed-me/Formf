from Formf import Form
from Formf.fields import Date


class EventForm(Form):
    event_date = Date(dateformat="%d.%m.%Y")


form = EventForm({"event_date": "10.01.2020"})
print(form.is_valid())
print(form.cleaned_data)
print(form.errors)
