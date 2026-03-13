from Formf.Core.errors import ValidationError

class Min:
    def __init__(self, minimum):
        self.minimum = minimum

    def __call__(self, value):
        if value < self.minimum:
            return ValidationError(
                code="Min",
                meta={"Min": self.minimum},
                value={"Input": value}
            )
        return None