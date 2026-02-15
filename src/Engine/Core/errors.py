# errors.py
class ValidationError(Exception):
    def __init__(self, code: str, message: str = None, meta=None):
        self.code = code
        self.message = message
        self.meta = meta or {}

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "meta": self.meta
        }
    
    def __repr__(self):
        return f"{self.code}({self.meta})"