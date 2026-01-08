from Core.errors import ValidationError
from datetime import datetime

class Date:

    def __init__(self, format):
        self.format = format
        self.strptformat = parser(format)

    def __call__(self, value):
        try:
            parsed = datetime.strptime(value, self.strptformat).date()
            return parsed
        
        except ValueError:
             return ValidationError(
                  code=Date,
                  message="Expected other Format",
                  meta=self.format
             )

def parser(format):
        
        FORMAT_MAP = {
            "YYYY": "%Y",
            "YY": "%y",
            "DD": "%d",
            "MM": "%m",
            
        }
        for token in sorted(FORMAT_MAP, key=len, reverse=True):
            format = format.replace(token, FORMAT_MAP[token])
        return print(format)