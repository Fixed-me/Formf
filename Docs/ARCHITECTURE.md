# Architecture

This document describes the current architecture of Formf. As the project is still a work in progress, parts of this design may evolve.

---

## Purpose of This Document

This file explains **why** Formf is built the way it is.

It is intended for:
- my future self
- others

User-facing usage is documented in `README.md`.
Only concepts relevant to design and structure are covered here.

---

## Design Goals

The Form Engine is designed around the following principles:

- Declarative form definitions
- Clear separation of concerns
- Minimal inheritance complexity
- Explicit and predictable validation behavior
- Extensibility without breaking existing APIs

---

## Architecture

```

Formf
└── Core
└── Fields
└── Validators
└──Validationerrors

````
---

## Forms

### Responsibility

A `Form`:
- acts as a container for Fields
- coordinates validation
- aggregates validation errors

A `Form` does **not**:
- perform validation logic itself
- know details about specific validators
- enforce field-level rules

---

## Meta Class Usage

### Why Meta Classes?

Forms use a meta class to collect Field instances at class creation time.

This enables:
- declarative syntax
- deterministic field ordering
- separation of definition-time and runtime logic

Fields are discovered once when the Form class is created, not during validation.

---

## Fields

### Responsibility

A `Field`:
- represents a single input value
- defines type and conversion logic
- owns its validators
- maps standard keyword arguments to validators

Fields are the **primary validation unit**.

---

### Standard Validators

Many validators can be defined directly via Field keyword arguments:

```python
String(minLength=3, maxLength=20)
````

Design rationale:

* common validation rules should be concise
* avoid verbose validator lists for simple cases
* keep forms readable

Internally, these keyword arguments are converted into validator instances.

---

## Validators

### Responsibility

A `Validator`:

* validates a single rule
* is stateless
* operates on a single value
* returns a `ValidationError` on failure

Validators do not:

* know about Forms
* know about other Fields
* modify values

This isolation makes validators:

* easy to test
* reusable
* composable

---

## Validation Errors

### Why Objects Instead of Strings?

Validation errors are represented as objects, not strings.

```python
ValidationError(
    code="min_length",
    message="Value is too short",
    meta={"min": 3}
)
```

Benefits:

* machine-readable error codes
* frontend-friendly metadata
* support for localization
* structured error aggregation

---

## Validation Flow

```md
Input Data
  ↓
Form receives input
  ↓
Form iterates over declared Fields
  ↓
Field extracts its value from input
  ↓
Field performs type conversion
  ↓
Field builds validators
  (explicit validators + standard kwargs)
  ↓
Field runs validators sequentially
  ↓
Validator validates one rule
  ↓
Validator returns ValidationError or None
  ↓
Field collects validation errors
  ↓
Field returns its errors to Form
  ↓
Form aggregates errors by field name
  ↓
Form exposes validation result



Validation is explicit and predictable.
No implicit cross-field validation exists at this stage.
```
---

## Public API vs Internal Implementation

The public API consists of:

* symbols exported via `Formf.__init__`
* documented Field parameters
* documented validator behavior

Everything else is considered internal and may change without notice.

Meta classes, internal helpers, and mapping logic are **not** part of the public API.

---

## Extensibility Strategy

The engine is designed to be extended by:

* adding new Field types
* adding new Validators
* composing existing validators

Inheritance-heavy extension is intentionally avoided.

---

## Architectural Stability

This architecture is expected to remain stable at the conceptual level.

Internal refactors are acceptable as long as:

* the public API remains consistent
* validation behavior remains predictable
* error structure is preserved
