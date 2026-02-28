from Formf.Core.errors import ValidationError


class Equals:
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, form):
        if form.cleaned_data.get(self.field1) != form.cleaned_data.get(self.field2):
            return ValidationError(
                code="Equalsform",
                message=f"The given fields should be equal",
                meta={'Field1': self.field1, 'Field2': self.field2},
            )
        return None
