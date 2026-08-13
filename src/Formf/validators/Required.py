from Formf.Core.errors import ValidationError

class Required:

    def __init__(self, required):
        self.required = required

    def __call__(self, value):
            if self.required and (value is None):
                return ValidationError(
                    "required",
                    meta={"Required": self.required},
                    value={"Input": value}

                )

            return False