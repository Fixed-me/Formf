from Formf.Core.errors import ValidationError

class Lowercase(object):
    def __init__(self, lowercase):
        self.lowercase = lowercase

    def __call__(self, value):
        if not value == value.lower():
            return ValidationError(
                code="Lowercase",
                meta={"Lowercase": self.lowercase},#
                value={"Input": value}
            )
        return None