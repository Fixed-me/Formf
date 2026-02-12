from Engine.Core.errors import ValidationError

class NotEquals:

    def __init__(self, equals):
        self.equals = equals

    def __call__(self, value):
        
        if not value != self.equals:
            return ValidationError(
                code="Equals",
                message="Values match but should not match",
                meta=self.equals
            )
        return None