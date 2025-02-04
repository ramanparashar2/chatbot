class NotFoundError(Exception):
    """Exception raised when a resource is not found."""
    pass

class BadRequestError(Exception):
    """Exception raised for bad requests."""
    pass

class UnauthorizedError(Exception):
    """Exception raised for unauthorized access."""
    pass

class InternalServerError(Exception):
    """Exception raised for internal server errors."""
    pass
