"""
decorators.py

This module provides custom decorators for the Flask application. Currently, it includes
a decorator for exception handling. The decorators are used to wrap view functions and
manage common cross-cutting concerns, such as error handling.

Decorators:
- handle_exceptions: A decorator that wraps a function to handle any exceptions that
  occur during its execution. It logs the error and returns a standardized error response
  to the client.

Dependencies:
- functools: Provides the `wraps` decorator to preserve the metadata of the original function.
- utils.config: Imports the `logger` object for logging error messages.

Usage:
Apply the `handle_exceptions` decorator to view functions to ensure that any exceptions
raised within those functions are properly handled and logged.

Example:
    @handle_exceptions
    def some_view_function():
        # View function logic
        pass
"""

from functools import wraps
from .config import logger


def handle_exceptions(f):
    """
    A decorator to handle exceptions that occur during the execution of a function.

    This decorator catches any exceptions raised by the wrapped function, logs the error
    message, and returns a standardized error response indicating a server error.

    Args:
        f (function): The function to be wrapped by the decorator.

    Returns:
        function: A wrapper function that handles exceptions and provides a consistent
        error response.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            return {"success": False, "message": "Server Error !!!"}

    return wrapper