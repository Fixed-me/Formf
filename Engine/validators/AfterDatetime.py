from Engine.Core.errors import ValidationError
from datetime import datetime

class After:

    def __init__(self, after, dateformat=None):
        self.after = after
        self.date_format = self.parser(dateformat) if dateformat else self.parser("YYYY-MM-DD") # Standart Format
        self.after_datetime = datetime.strptime(self.after, self.date_format)

    def __call__(self, value):

        value_date = datetime.strptime(value, self.date_format)
        if not value_date > self.after_datetime:
            return ValidationError(
                code="After datetime",
                message=f"The Date is not after the Expected date",
                meta={"After": self.after}
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