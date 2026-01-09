import re
from Engine.Core.errors import ValidationError

class URL:
    def __init__(self, regex):
        self.pattern = re.compile(regex)

    def __call__(self, value):
        if not self.pattern.match(value):
            return ValidationError(
                code="Url",
                message="Invalid Url",
                meta={"Pattern": self.pattern}
            )
        return None
