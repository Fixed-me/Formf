
# Form Engine

**Work in Progress**  
This Form Engine is currently under active development.  
APIs, validation behavior, and internal structures may change.

---

## Overview

The Form Engine is a modular Python framework for defining, validating, and processing forms.  
It is built around **Fields**, **Validators**, and a central **Form** class that ties everything together.

The goal is to make forms **declarative**, **extensible**, and **easy to test**.

---

## Installation

## User
```md
git clone https://github.com/Fixed-me/Form-Engine.git
cd Form-Engine
pip install -e .
````

## Development
Requirements:

- python 3.10+
- uv

Install uv:
https://astral.sh/uv

Setup Project:
```md
git clone https://github.com/Fixed-me/Form-Engine.git
cd Form-Engine
uv sync --extra dev
uv run pytest #to Test everything
```

---
## Core Concepts

### Form

A `Form` is a class composed of multiple Fields.

```python
from Formf import Form
from Formf.Fields import String, Integer
from Formf.Validators import Min

class UserForm(Form):
  name = String(minLength=3)
  password = Integer(validators=[Min(8)])
````

* Each form automatically collects all defined fields
* Validation is performed field by field
* Errors are returned in a structured format

---

### Fields

Fields represent individual input values, including type handling, conversion, and validation.

Currently available Fields:

* `Bool`
* `Date`
* `Float`
* `Integer`
* `List`
* `String`

Example:

```python
name = String()
age = Integer()
```

---

### Validators

Validators ensure that values meet specific rules.
They can be used **explicitly** or via **built-in (standard) validators**.

#### Explicit Validators

```python
from Formf.Fields import String
from Formf.Validators import MinLength

name = String(validators=[MinLength(3)])
```

#### Standard Validators (Shortcuts)

Many validators are available directly as keyword arguments on a Field:

```python
name = String(minLength=3)
email = String(email=True)
```

Internally, these arguments are automatically converted into validator instances.

### Field Standard Validators

All Fields provide a set of built-in standard validators that can be enabled
or configured directly via keyword arguments.

These validators exist on **every Field type** and are part of the public API.

---

#### Default Behavior

Unless explicitly overridden, all Fields behave as follows:

- `required = True`
- `nullable = True`
- `blank = False`

This means:
- a field is required by default
- `None` is accepted by default
- empty values (e.g. empty strings) are **not** accepted by default

---

#### Available Standard Validators

- `required`
- `requiredIf`
- `nullable`
- `blank`
- `default`

---

#### Usage

```python
from Formf import Form
from Formf.Fields import String, Integer


class ExampleForm(Form):
  name = String(
    default="default")  # required=True, nullable=True, blank=False and Field is None and default is set take the default value
  nickname = String(blank=True)  # allows empty string
  age = Integer(nullable=False)  # None is not allowed
  email = String(requiredif=(name, True))  # email is only required if name is not None
```

---

## Available Validators

### General

* `Equals`
* `NotEquals`
* `InList`
* `NotInList`
* `Choices`
* `Pattern`
* `Regex`

### String

* `minlength`
* `maxlength`
* `Lowercase`
* `Uppercase`
* `Email`
* `Url`

### Integer / Number

* `Min`
* `Max`

### Bool

* `Bool`

### Date / Datetime

* `BeforeDatetime`
* `AfterDatetime`
* `DateFormat`

---

## Validation Errors

Each validator returns a `ValidationError` object on failure.

Structure:

```python
ValidationError(
    code="validator_name",
    message="A default error message",
    meta={
        "name": expected_value
    }
)
```

Properties:

* **code**
  Machine-readable error code (e.g. for frontends or translations)

* **message**
  default error message

* **meta**
  Additional context (e.g. expected values or limits)

---

## Example: More Complex Form

```python
from Formf import Form
from Formf.Fields import String, Integer
from Formf.Validators import Min


class RegisterForm(Form):
  username = String(
    minlength=3,
    maxlength=20
  )

  password = Integer(
    validators=[Min(8)]
  )
```

---

## Architecture (Short Overview)

* `Form`
  Coordinates fields and validation

* `Field`
  Holds type, value, validators, and standard options

* `Validator`
  Isolated validation rules, independently testable

* `ValidationError`
  Unified error representation

---

## Current Status

Basic field types implemented

Modular validator system

Built-in validators per field

Documentation in progress

Tests in progress

API not yet 100% stable

---

## Planned Features (Ideas)

* Cross-field validation (e.g. `password == password_repeat`)
* Multilingual error messages
* Custom error messages per validator
* JSON / dict export of validation errors
* Optional strict parsing mode
* Async validation
* Schema export (e.g. for frontend usage)
* some JS/TS Extension 
---

## Contributing

Pull requests, ideas, and feedback are welcome.
Since the project is still evolving, please coordinate before making large changes.

---

## License

This project is licensed under the MIT License.

