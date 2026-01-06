import re
from Core.errors import ValidationError

class Regex:
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)
    
    def __call__(self, value, _):
        if not self.pattern.match(value):
            return ValidationError(
                "Invalid Format", "regex"
            )