from typing import Type, Union

from ..base import UFDLType

StrType = Union[str, Type[str]]
IntType = Union[int, Type[int]]
BoolType = Union[bool, Type[bool]]
FloatType = Union[float, Type[float]]

AnySimpleType = Union[StrType, IntType, BoolType, FloatType]

AnyUFDLType = Union[
    UFDLType, Type[UFDLType],
    StrType, IntType, BoolType, FloatType
]
