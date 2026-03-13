from Formf.Core.errors import ValidationError

class NotEquals:

    def __init__(self, equals):
        self.equals = equals

    def __call__(self, value):
        
        if not value != self.equals:
            return ValidationError(
                code="Not_Equals",
                meta={"Not_Equals": self.equals},
                value={"Input": value}
            )
        return None