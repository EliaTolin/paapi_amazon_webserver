class Error(Exception):
    """Base class for other exception"""
    code_message = "base_exception"

    def __dict__(self):
        return {"code_message": self.code_message}

    pass
