from Formf.Validators.InList import InList

class Choices:
    def __init__(self, choices):
        self.choices = choices
        self.values = {
            c[0] if isinstance(c, tuple) else c
            for c in choices
        }
        self._validator = InList(self.values)

    def __call__(self, value):
        return self._validator(value)
