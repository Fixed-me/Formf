from Formf.Core.errors import ValidationError

class RequiredIf:

    def __init__(self, requiredif):
        self.requiredif = requiredif

    def __call__(self, value, form=None):

        if self.requiredif is not None and self._requiredif_applies(form) and value is None:
            return ValidationError(
                code="requiredif",
                meta={"requiredif": self.requiredif},
                value={"Input": value}
            )
        return False

    def _requiredif_applies(self, form=None):
        if self.requiredif is None:
            return False

        # multiple conditions: any match means this field becomes required
        if isinstance(self.requiredif, list):
            return any(self._evaluate_requiredif_condition(c, form) for c in self.requiredif)

        return self._evaluate_requiredif_condition(self.requiredif, form)

    def _evaluate_requiredif_condition(self, condition, form):
        # backward compatible
        if isinstance(condition, tuple) and len(condition) == 2:
            field_name, expected = condition
            other_value = self._get_other_value(form, field_name)
            if isinstance(expected, bool):
                return self._field_is_filled(other_value) == expected
            return other_value == expected

        # callable support: lambda form -> bool
        if callable(condition):
            return bool(condition(form))

        # dict support
        if isinstance(condition, dict):
            fields = condition.get("fields")
            field_name = condition.get("field")

            if fields is None and field_name is not None:
                fields = [field_name]

            if not fields:
                return False

            values = [self._get_other_value(form, name) for name in fields]
            mode = condition.get("mode", "any")
            aggregator = any if mode == "any" else all

            if "equals" in condition:
                target = condition["equals"]
                return aggregator(v == target for v in values)

            if condition.get("not_empty", False):
                return aggregator(self._field_is_filled(v) for v in values)

            if condition.get("is_empty", False):
                return aggregator(not self._field_is_filled(v) for v in values)

        return False

    def _field_is_filled(self, value):
        return value not in (None, "")

    def _get_other_value(self, form, field_name):
        if form is None:
            return None
        return form.data.get(field_name)