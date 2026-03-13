from Formf.Core.errors import ValidationError
import re

class Pattern:
    REGEX = {
        "numeric": r"^\d+$",
        "alpha": r"^[A-Za-z]+$",
        "alphanumeric": r"^[A-Za-z0-9]+$",
        "email": r"^[^@]+@[^@]+\.[^@]+$"
    }
    def __init__(self, pattern):
        self.pattern_origin = pattern
        self.pattern = self.REGEX[pattern]
    
    def __call__(self, value):

        if self.pattern_origin not in self.REGEX:
            return ValidationError(
                code="Pattern",
                meta={"Pattern": self.REGEX},
                value={"Input": value}
            )

        if not re.fullmatch(self.pattern, value):
            return ValidationError(
                code="Pattern",
                meta={"Pattern": self.pattern},
                value = {"Input": value}
            )
        return None