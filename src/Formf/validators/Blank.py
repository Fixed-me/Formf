from Formf.Core.errors import ValidationError
class Blank:

    def __init__(self, blank):
        self.blank = blank

    def __call__(self, value):
        if self.blank and isinstance(value, str) and value == "":
            return ValidationError(
                "blank",
                meta={"blank": self.blank},
                value={"Input": value}
            )
        return False