from Formf.Core.errors import ValidationError
from datetime import datetime

class Before:

    def __init__(self, before, dateformat="YYYY-MM-DD"):
        self.before = before
        self.date_format = self.parser(dateformat)
        self.before_datetime = datetime.strptime(self.before, self.date_format)

    def __call__(self, value):
        
        value = datetime.strptime(value, self.date_format)

        if not value < self.before_datetime:
            return ValidationError(
                code="Before",
                message="The Date is after the Expected date",
                meta={"Before": self.before}
            )
        return None

    # to change the input into a valid python format
    @staticmethod
    def parser(date_format):
        format_map = {
            "YYYY": "%Y",
            "YY": "%y",
            "DD": "%d",
            "MM": "%m",
        }
        # Sorting is needed, to replace YYYY and YY
        for token in sorted(format_map, key=len, reverse=True):
            date_format = date_format.replace(token, format_map[token])
        return date_format