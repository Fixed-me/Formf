# errors.py
class ValidationError(Exception):
    def __init__(self, code: str, value = None, meta=None, message: str = None):
        self.code = code
        self.value = value
        self.meta = meta or {}
        self.message = message

    def to_dict(self):
        return {
            "code": self.code,
            "meta": self.meta,
            "value": self.value,
            "message": self.message
        }
    
    def __repr__(self):
        return f"{self.code}({self.meta})"