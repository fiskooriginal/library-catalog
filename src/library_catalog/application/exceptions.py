class ApplicationException(Exception):
    def __init__(self, message: str) -> None:
        self.message = f"Application exception: {message}"
        super().__init__(self.message)
