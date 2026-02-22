import re
from Formf.Core.errors import (ValidationError)

class Regex:
    def __init__(self, regex):
        self.regex = re.compile(regex)
    
    def __call__(self, value):
        if not self.regex.match(value):
            return ValidationError(
                code="Regex", 
                message="Invalid Format",
                meta={"Format": self.regex}
            )
        return None