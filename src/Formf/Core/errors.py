# errors.py
class ValidationError(Exception):
    def __init__(self, code: str, value = None, meta=None):
        self.code = code
        self.value = value
        self.meta = meta or {}

    def to_dict(self):
        return {
            "code": self.code,
            "meta": self.meta,
            "value": self.value
        }
    
    def __repr__(self):
        return f"{self.code}({self.meta})"