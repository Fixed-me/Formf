from Formf.Core.errors import ValidationError

class MaxLength:
    def __init__(self, length):
        self.length = length
    
    def __call__(self, value):
        if len(value) > self.length:
            return ValidationError(
                code="Max-length",
                message="String is to long",
                meta={"max": self.length}
            )
        return None