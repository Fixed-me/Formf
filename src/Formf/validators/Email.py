from Formf.Core.errors import ValidationError

class Email:
    def __call__(self, value):
        if "@" not in value:
            return ValidationError(
                code="Email",
                meta={"Email": value},
                value={"Input": value}
            )
        return None
