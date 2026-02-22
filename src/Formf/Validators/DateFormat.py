from datetime import datetime
from Formf.Core.errors import ValidationError

class Dateformat:
    def __init__(self, dateformat="YYYY-MM-DD"):
        self.dateformat = dateformat
        self.strptformat = self.parser(dateformat)

    def __call__(self, value):

        try:
            datetime.strptime(value, self.strptformat)
            return None
        except ValueError:
            return ValidationError(
                code="Dateformat",
                message="Value has not the expected format",
                meta={"format": self.dateformat},
            )

    @staticmethod
    def parser(dateformat):
        format_map = {
            "YYYY": "%Y",
            "YY": "%y",
            "DD": "%d",
            "MM": "%m",
        }
        for token in sorted(format_map, key=len, reverse=True):
            dateformat = dateformat.replace(token, format_map[token])
        return dateformat