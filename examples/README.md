# Formf Examples

This folder contains runnable examples for common and advanced usage.

## Structure

- `fields/`:
  One example per field type.
- `validators/`:
  Explicit validator usage by validator category.
- `formvalidators/`:
  Cross-field validation examples (`form_validators`).
- `standardvalidators/`:
  Built-in field options such as `required`, `nullable`, `blank`, `default`, and advanced `requiredif` rules.

## How to run

From the project root:

```bash
PYTHONPATH=src python3 examples/fields/string_field.py
PYTHONPATH=src python3 examples/validators/general_validators.py
PYTHONPATH=src python3 examples/formvalidators/equals_formvalidator.py
PYTHONPATH=src python3 examples/standardvalidators/requiredif_dict_and_list.py
```

## Notes

- Form-level errors are returned under `errors["__all__"]`.
- `requiredif` supports tuple, callable, dict, and list-of-conditions.
- These examples are independent files so users can copy only what they need.
