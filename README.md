# Formf

**Work in Progress**  
APIs, validation behavior, and internal structures may change.

## Overview

Formf is a modular Python form validation framework.
It is built around:

- `Form` for orchestration
- `Field` for type conversion + field-level rules
- `validators` for reusable single-field checks
- `crossfieldvalidators` for cross-field checks

## Installation

### User

```bash
git clone https://github.com/Fixed-me/Formf.git
cd Formf
pip install -e .
```

### Development

Requirements:

- Python 3.10+
- `uv`

```bash
git clone https://github.com/Fixed-me/Formf.git
cd Formf
uv sync --extra dev
uv run pytest
```

## Core Concepts

### Form and Field at a glance

| Concept | Responsibility | Input | Output |
|---|---|---|---|
| `Form` | Collect fields, run validation, aggregate errors | `dict` data | `is_valid()`, `cleaned_data`, `errors` |
| `Field` | Convert raw value, run field validators | single value | converted value or field errors |
| `validator` | Validate one field rule | value | `ValidationError` or `None` |
| `crossfieldvalidator` | Validate relationships between fields | form instance | `ValidationError` or `None` |

### Validation flow

| Step | What happens |
|---|---|
| 1 | Form iterates through declared fields |
| 2 | Each field runs `to_python()`, default handling, built-in checks, and custom validators |
| 3 | `cleaned_data` is filled with valid field values |
| 4 | If no field-level errors exist, `crossfield_validators` are executed |
| 5 | Cross-field errors are stored under `errors["__all__"]` |

## Fields

Available field types:

| Field | Type conversion |
|---|---|
| `String` | value must be `str` (empty becomes `None`) |
| `Integer` | value is cast to `int` |
| `Float` | value must be `float` |
| `Bool` | value must be `bool` |
| `Date` | parses date strings with supported formats |
| `List` | value is cast to `list` |

### Shared field options

These options are available on all fields:

| Option | Default | Meaning |
|---|---|---|
| `strict` | `False` | strict type parsing (when supported by the field) |
| `required` | `True` | field must be present |
| `requiredif` | `None` | field becomes required when condition matches |
| `nullable` | `True` | allow `None` |
| `blank` | `False` | blank handling for string-like input |
| `default` | `None` | fallback value if input is missing/`None` |
| `validators` | `None` | list of additional validator instances |

### Field-specific shortcut options

| Field | Shortcut options |
|---|---|
| `String` | `minlength`, `maxlength` |
| `Integer` | `minvalue`, `maxvalue` |
| `Float` | `minvalue`, `maxvalue` |
| `Date` | `dateformat`, `before`, `after` |
| `Bool` | `value` |
| `List` | `listvalues`, `must_be_in`, `item_field` |

### Strict vs Lenient conversion (`to_python`)

| Field | Strict mode (`strict=True`) | Lenient mode (`strict=False`) |
|---|---|---|
| `String` | only accepts `str` | non-string values are converted with `str(value)` |
| `Integer` | only accepts `int` | accepts `float` and numeric strings (`"42"`) |
| `Float` | only accepts `float` | accepts `int` and numeric strings (`"3.14"`) |
| `Date` | accepts `datetime` or strict `%Y-%m-%d` string | accepts `datetime` or several common string date formats |
| `List` | only accepts `list` | also accepts `tuple` and `set` (converted to `list`) |
| `Bool` | accepts bool input only | currently still requires bool input; string/int coercion is limited in current implementation |

## List membership (simplified)

Use one list plus one mode flag:

```python
from Formf.fields import List

# all items must be in the provided list
allowed_tags = List(listvalues=["a", "b", "c"], must_be_in=True)

# all items must NOT be in the provided list
blocked_tags = List(listvalues=["x", "y"], must_be_in=False)
```

Legacy args are still accepted for compatibility:

- `inlist=...` (same as `listvalues=..., must_be_in=True`)
- `notinlist=...` (same as `listvalues=..., must_be_in=False`)

## `requiredif` (extended behavior)

`requiredif` now supports multiple condition styles.

### 1) Tuple: empty/not-empty or exact value

```python
email = String(requiredif=("name", True))        # required if name is not empty
suffix = String(requiredif=("middle_name", False))  # required if middle_name is empty
note = String(requiredif=("status", "approved")) # required if status == "approved"
```

### 2) Callable

```python
age = Integer(requiredif=lambda form: form.data.get("name") == "Alice")
```

### 3) Dict rule

```python
nickname = String(requiredif={"field": "name", "not_empty": True})
note = String(requiredif={"field": "status", "equals": "approved"})
suffix = String(requiredif={"field": "middle_name", "is_empty": True})
```

### 4) Multiple fields with mode

```python
reason = String(
    requiredif={"fields": ["role", "plan"], "equals": "pro", "mode": "any"}
)

alias = String(
    requiredif={"fields": ["first_name", "last_name"], "not_empty": True, "mode": "all"}
)
```

### 5) List of conditions (OR)

```python
support_note = String(
    requiredif=[
        ("status", "approved"),
        {"field": "role", "equals": "admin"},
    ]
)
```

## Validators

### Field validators (`Formf.validators`)

| Group | Validators |
|---|---|
| General | `Equals`, `NotEquals`, `InList`, `Choices`, `Pattern`, `Regex` |
| String | `MinLength`, `MaxLength`, `Lowercase`, `Uppercase`, `Email`, `Url` |
| Number | `Min`, `Max` |
| Bool | `Bool` |
| Date | `Before`, `After`, `Dateformat` |

For membership checks, prefer `InList(values, should_be_in=True/False)`.
`NotInList` remains available as a compatibility wrapper.

### Cross-field validators (`Formf.crossfieldvalidators`)

| Validator | Meaning | Error code |
|---|---|---|
| `Equals(field1, field2)` | `field1` must equal `field2` | `Equalsform` |
| `AfterDate(field1, field2)` | `field1` must be after `field2` | `AfterDateForm` |
| `BeforeDate(field1, field2)` | `field1` must be before `field2` | `BeforeDateForm` |

## Examples

### Basic form

```python
from Formf import Form
from Formf.fields import String, Integer
from Formf.validators import Min


class UserForm(Form):
    name = String(minlength=3)
    password = Integer(validators=[Min(8)])
```

### Cross-field form

```python
from Formf import Form
from Formf.fields import String
from Formf.crossfieldvalidators import Equals, BeforeDate


class RegisterForm(Form):
    password = String()
    password_repeat = String()
    start_date = String()
    end_date = String()

    crossfield_validators = [
        Equals("password", "password_repeat"),
        BeforeDate("start_date", "end_date"),
    ]


form = RegisterForm(
    {
        "password": "abc123",
        "password_repeat": "abc124",
        "start_date": "10.01.2020",
        "end_date": "09.01.2020",
    }
)

form.is_valid()  # False
form.errors
# {
#   "__all__": [
#     {"code": "Equalsform", ...},
#     {"code": "BeforeDateForm", ...}
#   ]
# }
```

## Validation Errors

Errors are exposed in a serializable dict format.

```python
{
    "field_name": [
        {
            "code": "validator_name",
            "message": "Error message",
            "meta": {"key": "value"}
        }
    ],
    "__all__": [
        {
            "code": "cross_field_error",
            "message": "Cross-field error message",
            "meta": {}
        }
    ]
}
```

`"__all__"` is reserved for form-level (cross-field) errors.

## Schema Export

Formf now provides a frontend-friendly schema export:

```python
schema = MyForm({}).to_schema()
```

### Export structure

| Key | Description |
|---|---|
| `form` | Form class name |
| `version` | Schema version (`"1.0"`) |
| `fields` | Field map with type/options/validators |
| `crossfield_validators` | Cross-field validator list |
| `errors_schema` | Contract for error payloads (`__all__` for form errors) |

### Field schema shape

Each field contains:

- `type`
- `required`
- `requiredif`
- `nullable`
- `blank`
- `default`
- `validators` (`[{name, params}]`)

### `requiredif` export notes

- Tuple condition exports as:
  - `{"type": "tuple", "field": "...", "expected": ...}`
- Dict condition exports as:
  - `{"type": "rule", "rule": {...}}`
- List condition exports as:
  - `{"type": "any", "conditions": [...]}`
- Callable condition exports as:
  - `{"type": "callable", "exportable": false, "name": "..."}`

### Example output

```python
{
  "form": "RegisterForm",
  "version": "1.0",
  "fields": {
    "password": {
      "type": "string",
      "required": True,
      "requiredif": None,
      "nullable": True,
      "blank": False,
      "default": None,
      "validators": [{"name": "MinLength", "params": {"length": 8}}]
    }
  },
  "crossfield_validators": [
    {"name": "Equals", "params": {"field1": "password", "field2": "password_repeat"}}
  ],
  "errors_schema": {
    "field_error_shape": {"code": "string", "message": "string|null", "meta": "object"},
    "form_error_key": "__all__"
  }
}
```

Schema examples are available in:

- `Docs/examples/schema/basic_schema_export.py`
- `Docs/examples/schema/advanced_schema_export.py`

## Testing

Run all tests:

```bash
pytest
```

Run cross-field tests only:

```bash
pytest src/Formf/Core/Tests/Crossfieldvalidators
```

## Current Status

- Field validation is implemented
- Cross-field validation is implemented via `crossfield_validators`
- Basic tests for field and crossfieldvalidators are in place
- API is still evolving

## Contributing

Pull requests, ideas, and feedback are welcome.

## License

MIT
