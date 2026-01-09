from datetime import datetime
from Engine.Core.errors import ValidationError

class Date:
    def __init__(self, date_format):
        self.date_format = date_format
        self.strptformat = self.parser(date_format)

    def __call__(self, value):
        try:
            datetime.strptime(value, self.strptformat).date()
            return None
        except (ValueError, TypeError):
            return ValidationError(
                code="Date",
                message="Expected other Format",
                meta={"format": self.date_format }
            )

    @staticmethod
    def parser(date_format):
        format_map = {
            "YYYY": "%Y",
            "YY": "%y",
            "DD": "%d",
            "MM": "%m",
        }
        # Sortierung ist wichtig, damit YYYY vor YY ersetzt wird
        for token in sorted(format_map, key=len, reverse=True):
            date_format = date_format.replace(token, format_map[token])
        return date_format
