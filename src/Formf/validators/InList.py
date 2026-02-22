from Formf.Core.errors import ValidationError

class InList:
    def __init__(self, listvalue):
        self.list = set(listvalue)

    def __call__(self, value):
        if value not in self.list:
            return ValidationError(
                code="InList",
                message="List not in origin List",
                meta={"List": self.list}
            )
        return None
