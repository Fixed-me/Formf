from Formf.Core.errors import ValidationError

class MinLength:
    def __init__(self, length):
        self.length = length

    def __call__(self, value):
        if len(value) < self.length:
            return ValidationError(
                code="Min_length",
                meta={"Min_length": self.length},
                value={"Input": value}
            )
        return None