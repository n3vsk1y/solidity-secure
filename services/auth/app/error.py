from typing import Any

class BaseAuthServiceError(Exception):
    def __init__(self, message: str, code: int | None, meta: Any):
        super().__init__(message)
        self.code = code
        self.meta = meta


class AuthServiceError(BaseAuthServiceError):
    def __init__(self, message: str, code: int | None, meta: Any = None):
        super().__init__(message, code, meta)


class EnvVariablesError(BaseAuthServiceError):
    def __init__(self, message: str, code: int | None, meta: Any = None):
        super().__init__(message, code, meta)