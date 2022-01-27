import builtins
from typing import Any

from wai.json.raw import RawJSONElement
from wai.json.schema import BOOL_SCHEMA, JSONSchema, constant, number, string_schema
from wai.common.serialisation.serialisers import IntSerialiser, FloatSerialiser, BoolSerialiser

from ._const import SIMPLE_TYPES
from ._format import format_type
from ._json import validate_with_schema
from ._type import AnyUFDLType, AnySimpleType

SERIALISERS = {
    int: IntSerialiser(),
    float: FloatSerialiser(),
    bool: BoolSerialiser()
}


def is_simple_type(type: AnyUFDLType) -> bool:
    return isinstance(type, SIMPLE_TYPES) or type in SIMPLE_TYPES


def get_simple_schema(type: AnySimpleType) -> JSONSchema:
    if isinstance(type, SIMPLE_TYPES):
        return constant(type)
    elif type is str:
        return string_schema()
    elif type in (int, float):
        return number(integer_only=type is int)
    elif type is bool:
        return BOOL_SCHEMA


def parse_simple_json_value(type: AnySimpleType, value: RawJSONElement) -> Any:
    validate_with_schema(get_simple_schema(type), value)
    return value


def format_json_value(type: AnySimpleType, value: Any) -> RawJSONElement:
    validate_with_schema(type, value)
    return value


def parse_simple_binary_value(type: AnySimpleType, value: bytes) -> Any:
    if isinstance(type, SIMPLE_TYPES):
        type_class = builtins.type(type)
        value = parse_simple_json_value(type_class, value)
        if value != type:
            raise ValueError(f"Expected {type_class}-const-type {format_type(type)} but got {format_type(value)}")
        return value
    elif type is str:
        return value.decode("UTF-8")
    else:
        return SERIALISERS[type].deserialise_from_bytes(value)


def format_simple_binary_value(type: AnySimpleType, value: Any) -> bytes:
    if isinstance(type, SIMPLE_TYPES):
        type_class = builtins.type(type)
        if value != type:
            raise ValueError(f"Expected {type_class}-const-type {format_type(type)} but got {format_type(value)}")
        return format_simple_binary_value(type_class, value)
    elif type is str:
        if not isinstance(value, str):
            raise ValueError(f"Value {value} is not a string")
        return value.encode("UTF-8")
    else:
        return SERIALISERS[type].serialise_to_bytes(value)
