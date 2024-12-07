class BaseError(Exception):
    def __init__(self, message: str, status: int, code: str, title: str):
        self.message = message
        super().__init__(self.message)
