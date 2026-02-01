from Engine.Core.errors import ValidationError

class Choices:

    def __init__(self, options):
        self.options = options

    def __call__(self, value):
        
        if value in self.options:
            return None
        else:
            return ValidationError(
                code="Choices",
                message="The Value is not in Choices",
                meta={"Choices": self.options}
            )