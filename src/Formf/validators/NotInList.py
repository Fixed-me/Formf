from Formf.validators.InList import InList

class NotInList:
    def __init__(self, listvalue):
        self.list = set(listvalue)
        self._validator = InList(listvalue, should_be_in=False)

    def __call__(self, value):
        return self._validator(value)

    def to_schema(self):
        return {
            "name": "NotInList",
            "params": {
                "list": sorted(self.list, key=str),
                "should_be_in": False,
            },
        }
