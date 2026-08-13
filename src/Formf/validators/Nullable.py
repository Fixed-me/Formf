from Formf.Core.errors import ValidationError

class Nullable:

    def __init__(self, nullable):
        self.nullable = nullable

    def __call__(self, value):

        if not self.nullable and (value is None):
            return ValidationError(
                code="nullable",
                meta={"nullable": self.nullable}
            )
        return False