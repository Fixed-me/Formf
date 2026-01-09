from Engine.Core.errors import ValidationError

class Min:
    def __init__(self, minimum):
        self.minimum = minimum

    def __call__(self, value):
        if value < self.minimum:
            return ValidationError(
                code="Min",
                message="Integer is to small",
                meta={"Min": self.minimum}
            )
        return None