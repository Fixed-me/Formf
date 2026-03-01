import re

class Schema:
    @staticmethod
    def serialize_value(value):
        if value is None or isinstance(value, (bool, int, float, str)):
            return value

        if isinstance(value, re.Pattern):
            return value.pattern

        if isinstance(value, (list, tuple, set, frozenset)):
            return [Schema.serialize_value(v) for v in value]

        if isinstance(value, dict):
            return {
                str(k): Schema.serialize_value(v)
                for k, v in value.items()
            }

        if callable(value):
            return {
                "type": "callable",
                "exportable": False,
                "name": getattr(value, "__name__", value.__class__.__name__),
            }

        if hasattr(value, "isoformat") and callable(value.isoformat):
            try:
                return value.isoformat()
            except Exception:
                pass

        return repr(value)

    @staticmethod
    def serialize_requiredif_condition(condition):
        if isinstance(condition, tuple) and len(condition) == 2:
            field_name, expected = condition
            return {
                "type": "tuple",
                "field": field_name,
                "expected": Schema.serialize_value(expected),
            }

        if callable(condition):
            return Schema.serialize_value(condition)

        if isinstance(condition, dict):
            return {
                "type": "rule",
                "rule": Schema.serialize_value(condition),
            }

        return {
            "type": "literal",
            "value": Schema.serialize_value(condition),
        }

    @staticmethod
    def serialize_requiredif(requiredif):
        if requiredif is None:
            return None

        if isinstance(requiredif, list):
            return {
                "type": "any",
                "conditions": [
                    Schema.serialize_requiredif_condition(c)
                    for c in requiredif
                ],
            }

        return Schema.serialize_requiredif_condition(requiredif)

    @staticmethod
    def serialize_validator(validator):
        if hasattr(validator, "to_schema") and callable(validator.to_schema):
            raw = validator.to_schema()
            if isinstance(raw, dict):
                if "name" not in raw:
                    raw["name"] = validator.__class__.__name__
                return Schema.serialize_value(raw)

        params = {
            key: Schema.serialize_value(value)
            for key, value in getattr(validator, "__dict__", {}).items()
            if not key.startswith("_")
        }
        return {
            "name": validator.__class__.__name__,
            "params": params,
        }
