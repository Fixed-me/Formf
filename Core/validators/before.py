from Core.errors import ValidationError

class Before:

    def __init__(self, before):
        self.before = before

    def __call__(self, value):
        
        if not value < self.before:
            return ValidationError(
                code="Before",
                message="The Date is after the Expected date",
                meta=self.before
            )

