from fastapi import status


class ValidationException(Exception):
    def __init__(
        self, reason: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> None:
        self.status_code = status_code
        self.reason = reason
        super().__init__(reason, status_code)
