from Engine.Core.errors import ValidationError

class InList:
    def __init__(self, list, inlist):
        self.list = list
        self.inlist = inlist

    def __call__(self, value):
        if value not in self.list:
                return ValidationError(
                    code="List",
                    message="List in origin List",
                    meta={"List": self.list, "inList": self.inlist}
            )
        return None
