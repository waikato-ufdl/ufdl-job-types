from typing import Type, Union

from .base import UFDLType

AnyUFDLType = Union[UFDLType, int, str, Type[UFDLType], Type[int], Type[str]]
