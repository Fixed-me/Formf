from Formf.Core.errors import ValidationError

class Max:
    def __init__(self, maximum):
        self.maximum = maximum

    def __call__(self, value):
        if value > self.maximum:
            return ValidationError(
                code="Max",
                meta={"Max": self.maximum},
                value={"Input": value}
            )
        return None
