"""
The base hierarchy of types that the UFDL server uses for jobs.
"""
from ._FiniteJSONType import FiniteJSONType
from ._NamedServerType import NamedServerType
from ._ServerResidentType import ServerResidentType
from ._UFDLJSONType import UFDLJSONType
from ._UFDLType import UFDLType, TypeArgsType, InputType, OutputType
from ._ValueType import (
    ValueType,
    TRUE_CONST_SYMBOL,
    FALSE_CONST_SYMBOL,
    VALUE_TYPES,
    AnyValueType,
    String,
    Integer,
    Float,
    Boolean
)
