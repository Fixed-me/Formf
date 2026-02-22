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
        if pattern not in self.REGEX:
            raise ValueError(code="Pattern", message="Unknown pattern {pattern}", meta={"Pattern": self.REGEX})
        self.pattern = self.REGEX[pattern]
    
    def __call__(self, value):
        
        if not re.fullmatch(self.pattern, value):
            return ValidationError(
                code="Pattern",
                message="Expected other pattern",
                meta={"Pattern": self.pattern}
            )
        return None