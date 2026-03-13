from Formf.Core.errors import ValidationError

class Equals:

    def __init__(self, equals):
        self.equals = equals

    def __call__(self, value):
        
        if value != self.equals:
            return ValidationError(
                code="Equals",
                meta={"Equals": self.equals},
                value={"Input": value}
            )
        return None