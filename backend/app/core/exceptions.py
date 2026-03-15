# backend/app/core/exceptions.py


class BusinessRuleError(Exception):
    """Raised when a business rule is violated."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(Exception):
    """Raised when a requested resource does not exist."""
    def __init__(self, resource: str, resource_id: str = ""):
        self.message = f"{resource} not found" + (f": {resource_id}" if resource_id else "")
        super().__init__(self.message)


class UnauthorizedError(Exception):
    """Raised when a user tries to access a resource they don't own."""
    def __init__(self, message: str = "Unauthorized"):
        self.message = message
        super().__init__(message)
