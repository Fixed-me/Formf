from Formf.Core.errors import ValidationError

class Uppercase:

    def __init__(self, uppercase):
        self.uppercase = uppercase

    def __call__(self, value):

        if not value == value.upper():
            return ValidationError(
                code="Uppercase",
                message=f"The Value is not uppercase.",
                meta={"Uppercase": self.uppercase}
            )
        return None