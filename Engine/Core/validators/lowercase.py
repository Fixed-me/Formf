from Engine.Core.errors import ValidationError

class Lowercase(object):
    def __init__(self, lowercase):
        self.lowercase = lowercase

    def __call__(self, value):
        if not value == value.lower():
            return ValidationError(
                code="Lowercase",
                message=f"The value is not lowercase",
                meta={"Lowercase": self.lowercase}
            )
        return None