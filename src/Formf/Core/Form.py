# form.py
from Formf.Core.Field import Field
from Formf.Core.schema import Schema
import json
import os

class FormMeta(type):
    def __new__(cls, name, bases, attrs):
        # collect all fields that where created in the class
        fields = {}

        # Extract all fields with the class Definition,
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

        # validate all fields separately from each other
        for name, field in self._fields.items():
            raw = self.data.get(name)

            # clean does Type conversion and validation
            value, errs = field.clean(raw, form=self)

            if errs:
                self._errors.setdefault(name, []).extend(errs)
            elif value is not None:
                self.cleaned_data[name] = value

        # the Form is only valid if no error occurred
        if not self._errors:
            self._run_crossfield_validators()

        return not self._errors

    @staticmethod
    def resolve_messages(code, language):

        base_dir = os.path.dirname(__file__)

        file = f"{language}.json"
        path = os.path.join(base_dir, "MESSAGE_TEMPLATES", file)

        with open(path, encoding="utf-8") as msg:
            template = json.load(msg)

        data = template[code]

        return data

    def errors(self, messages=True, language="en"):

        # change Error objects in a serializable format
        result = {}

        for field_name, errors in self._errors.items():

            result[field_name] = []

            for err in errors:
                err_dict = err.to_dict()

                if messages:
                    err_dict["message"] = self.resolve_messages(err.code, language)

                result[field_name].append(err_dict)

        return result

    def _run_crossfield_validators(self):
        for validator in getattr(self, "crossfield_validators", []):
            error = validator(self)
            if error is not None:
                self._errors.setdefault("__all__", []).append(error)

    def to_schema(self):
        return {
            "form": self.__class__.__name__,
            "version": "1.0",
            "fields": {
                field_name: field.to_schema()
                for field_name, field in self._fields.items()
            },
            "crossfield_validators": [
                Schema.serialize_validator(v)
                for v in getattr(self, "crossfield_validators", [])
            ],
            "errors_schema": {
                "field_error_shape": {
                    "code": "string",
                    "meta": "object",
                    "value": "object",
                    "message": "string|null",

                },
                "form_error_key": "__all__",
            },
        }
