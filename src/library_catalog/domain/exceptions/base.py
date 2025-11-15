class DomainException(Exception):
    def __init__(self, message: str) -> None:
        self.message = f"Domain exception: {message}"
        super().__init__(self.message)
