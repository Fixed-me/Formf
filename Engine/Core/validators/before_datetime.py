from Engine.Core.errors import ValidationError
from datetime import datetime

class Before:

    def __init__(self, before, date_format):
        self.before = before
        self.date_format = self.parser(date_format)
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