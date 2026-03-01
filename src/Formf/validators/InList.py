from Formf.Core.errors import ValidationError

class InList:
    def __init__(self, listvalue, *, should_be_in: bool = True):
        self.list = set(listvalue)
        self.should_be_in = should_be_in

    def __call__(self, value):
        values = value if isinstance(value, (list, tuple, set)) else [value]

        if self.should_be_in:
            invalid = [v for v in values if v not in self.list]
            if invalid:
                return ValidationError(
                    code="InList",
                    message="List not in origin List",
                    meta={"List": self.list, "Invalid": invalid}
                )
        else:
            blocked = [v for v in values if v in self.list]
            if blocked:
                # keep historical error code for backward compatibility
                return ValidationError(
                    code="NoInList",
                    message="List in origin List",
                    meta={"List": self.list, "Blocked": blocked}
                )

        return None

    def to_schema(self):
        return {
            "name": "InList",
            "params": {
                "list": sorted(self.list, key=str),
                "should_be_in": self.should_be_in,
            },
        }
