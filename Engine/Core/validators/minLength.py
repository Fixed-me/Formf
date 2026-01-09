from Engine.Core.errors import ValidationError

class MinLength:
    def __init__(self, length):
        self.length = length

    def __call__(self, value):
        if len(value) < self.length:
            return ValidationError(
                code="min_length",
                message="String is to short",
                meta={"min": self.length}
            )
        return None