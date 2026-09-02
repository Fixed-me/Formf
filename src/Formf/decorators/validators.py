class ValidatorDefinition:
    def __init__(self, field_name, function):
        self.field_name = field_name
        self.name = function.__name__
        self.function = function

def validators(name):
    def decorator(func):

        return ValidatorDefinition(name, func)

    return decorator



