from Engine.Core.errors import ValidationError
import re

class Pattern:

    def __init__(self, pattern):
        self.pattern = pattern
    
    def __call__(self, value):
        
        if not re.fullmatch(self.pattern, value):
            return ValidationError(
                code="Pattern",
                message="Expected other pattern",
                meta={"Pattern": self.pattern}
            )
        return None