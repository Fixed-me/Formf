# Formf

**Work in Progress**  
APIs, validation behavior, and internal structures may change.

## Overview

Formf is a modular Python form validation framework.
It is built around:

- `Form` for orchestration
- `Field` for type conversion + field-level rules
- `validators` for reusable single-field checks
- `formvalidators` for cross-field checks

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
| `formvalidator` | Validate relationships between fields | form instance | `ValidationError` or `None` |

### Validation flow

| Step | What happens |
|---|---|
| 1 | Form iterates through declared fields |
| 2 | Each field runs `to_python()`, default handling, built-in checks, and custom validators |
| 3 | `cleaned_data` is filled with valid field values |
| 4 | If no field-level errors exist, `form_validators` are executed |
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
| `List` | `inlist`, `notinlist` |

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
| General | `Equals`, `NotEquals`, `InList`, `NotInList`, `Choices`, `Pattern`, `Regex` |
| String | `MinLength`, `MaxLength`, `Lowercase`, `Uppercase`, `Email`, `Url` |
| Number | `Min`, `Max` |
| Bool | `Bool` |
| Date | `Before`, `After`, `Dateformat` |

### Cross-field validators (`Formf.formvalidators`)

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
from Formf.formvalidators import Equals, BeforeDate


class RegisterForm(Form):
    password = String()
    password_repeat = String()
    start_date = String()
    end_date = String()

    form_validators = [
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

## Testing

Run all tests:

```bash
pytest
```

Run cross-field tests only:

```bash
pytest src/Formf/Core/Tests/Formvalidators
```

## Current Status

- Field validation is implemented
- Cross-field validation is implemented via `form_validators`
- Basic tests for field and formvalidators are in place
- API is still evolving

## Contributing

Pull requests, ideas, and feedback are welcome.

## License

MIT
