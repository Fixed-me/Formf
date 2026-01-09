from Engine.Core.errors import ValidationError

class Email:
    def __call__(self, value):
        if "@" not in value:
            return ValidationError(
                code="Email",
                message="@ not in Email",
                meta={"Email": value}
            )
        return None
