from typing import Any

from ..base import UFDLType
from ._const import SIMPLE_TYPES


def is_ufdl_type(value: Any) -> bool:
    """
    Checks if a given value is a UFDL type.

    :param value:
                The value to check.
    """
    if isinstance(value, type):
        return (
                issubclass(value, UFDLType)
                or value in SIMPLE_TYPES
        )

    return isinstance(value, (UFDLType, *SIMPLE_TYPES))
