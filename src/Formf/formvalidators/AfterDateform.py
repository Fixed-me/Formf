from Formf.Core.errors import ValidationError


class AfterDate:
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, form):
        if form.cleaned_data.get(self.field1) < form.cleaned_data.get(self.field2):
            return ValidationError(
                code="AfterDateForm",
                message=f"Startdate should be after Enddate ",
                meta={'Startdate': self.field1, 'Enddate': self.field2},
            )
        return None
