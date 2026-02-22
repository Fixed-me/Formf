from Formf.Core.errors import ValidationError

class NotInList:
    def __init__(self, listvalue):
        self.list = set(listvalue)

    def __call__(self, value):
        if value in self.list:
            return ValidationError(
                code="NoInList",
                 message="List in origin List",
                meta={"List": self.list}
            )
        return None