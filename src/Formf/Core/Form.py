# form.py
from Formf.Core.Field import Field

class FormMeta(type):
    def __new__(cls, name, bases, attrs):
        # collect all Fields that where created in the class
        fields = {}

        # Extract all Fields with the class Definition,
        # to process them
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                # Fieldname == Kwarg in class
                value.name = key
                fields[key] = value

                # delete from attr prevents, the Field to
                # exists as normal class
                del attrs[key]

        # _fields to describe the Form
        attrs["_fields"] = fields

        return super().__new__(cls, name, bases, attrs)


class Form(metaclass=FormMeta):
    def __init__(self, data):
        # raw Input (like from the Form, or a request)
        self.data = data

        # save Validationerrors for every Field
        self._errors = {}

        # save all validated data
        self.cleaned_data = {}

    def is_valid(self):
        # validate all Fields separately from each other
        for name, field in self._fields.items():
            raw = self.data.get(name)

            # clean does Type conversion and validation
            value, errs = field.clean(raw)

            if errs:
                self._errors.setdefault(name, []).extend(errs)
            elif value is not None:
                self.cleaned_data[name] = value

        # the Form is only valid if no error occurred
        if not self._errors:
            self._run_form_validators()

        return not self._errors

    @property
    def errors(self):
        # change Error objects in a serializable format
        result = {}

        for field_name, errors in self._errors.items():
            result[field_name] = [err.to_dict() for err in errors]

        return result

    def _run_form_validators(self):
        for validator in getattr(self, "form_validators", []):
            validator(self)