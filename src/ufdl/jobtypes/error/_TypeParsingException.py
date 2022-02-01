from typing import Any


class TypeParsingException(Exception):
    """
    Exception for when there is an error parsing a type-string.
    """
    def __init__(self, type_string: str, cause: Any = None):
        message = f"Error parsing type-string \"{type_string}\""

        if cause is not None:
            message += f": {cause}"

        super().__init__(message)
