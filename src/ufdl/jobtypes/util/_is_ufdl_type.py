from typing import Any

from ..base import UFDLType


def is_ufdl_type(value: Any) -> bool:
    """
    Checks if a given value is a UFDL type.

    :param value:
                The value to check.
    """
    if isinstance(value, type):
        return (
                issubclass(value, UFDLType)
                or value is str
                or value is int
        )

    return isinstance(value, (UFDLType, str, int))
