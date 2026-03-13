from Formf.Core.errors import ValidationError

class Bool:
    def __init__(self, value: bool):
        self.bool = value

    def __call__(self, value):
        if self.bool != value:
            return ValidationError(
                code="Bool",
                meta={"Bool": self.bool},
                value={"Input": value}
            )
        return None
