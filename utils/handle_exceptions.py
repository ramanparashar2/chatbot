from functools import wraps
from fastapi import HTTPException

from error.error_handler import ErrorHandler


def handle_exceptions(func):
    """Decorator to handle exceptions and raise HTTP errors."""    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            error_handler = ErrorHandler()
            error_handler.handle_exception(e)
        
    return wrapper
