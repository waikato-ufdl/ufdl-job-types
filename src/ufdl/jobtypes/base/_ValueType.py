from typing import Optional, Tuple, Type, Union
from weakref import WeakValueDictionary

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, any_of, string_schema, number, BOOL_SCHEMA, constant

from ._UFDLJSONType import UFDLJSONType

# Types
StrType = Union[str, Type[str]]
IntType = Union[int, Type[int]]
BoolType = Union[bool, Type[bool]]
FloatType = Union[float, Type[float]]
AnyValueType = Union[StrType, IntType, BoolType, FloatType]
AnyValue = Union[str, float, int, bool]

# String representations of the true and false value-types
TRUE_CONST_SYMBOL = "@true"
FALSE_CONST_SYMBOL = "@false"

# The set of Python types that are considered UFDL types. Values of these types
# are considered sub-types of their respective type.
VALUE_TYPES = str, int, float, bool


class ValueType(UFDLJSONType[Tuple[()], AnyValue, AnyValue]):
    _instances = WeakValueDictionary()
    _value: Optional[AnyValueType] = None

    @classmethod
    def value(cls) -> Optional[AnyValueType]:
        return cls._value

    @staticmethod
    def generate_subclass(value: AnyValueType) -> Type['ValueType']:
        if value in ValueType._instances:
            return ValueType._instances[value]

        schema = (
            string_schema() if value is str
            else number(integer_only=True) if value is int
            else number() if value is float
            else BOOL_SCHEMA if value is bool
            else constant(value) if isinstance(value, VALUE_TYPES)
            else None
        )

        if schema is None:
            raise Exception(f"Can't generate value-schema for {value}")

        base_class = (
            ValueType[Tuple[()], value, value] if isinstance(value, type)
            else ValueType.generate_subclass(type(value))
        )

        class SpecialisedValueType(base_class):
            _value = value

            @property
            def json_schema(self) -> JSONSchema:
                return schema

            def __str__(self) -> str:
                # Simple type parameters are represented by their type name
                if value in VALUE_TYPES:
                    return self.format_type_class_name()

                # String-value type arguments are single-quoted, with internal single-quotes backslash-escaped
                if isinstance(value, str):
                    formatted_str_type_arg = value.replace("'", "\\'")
                    return f"'{formatted_str_type_arg}'"

                # Bool-value types have special constant representations
                if value is True:
                    return TRUE_CONST_SYMBOL
                elif value is False:
                    return FALSE_CONST_SYMBOL

                # Numeric-value type arguments are just the number itself
                if isinstance(value, (int, float)):
                    return str(value)

                raise Exception("Should never reach here")

        ValueType._instances[value] = SpecialisedValueType

        return SpecialisedValueType

    def parse_json_value(self, value: RawJSONElement):
        self.validate_with_schema(value)
        return value

    def format_python_value_to_json(self, value) -> RawJSONElement:
        self.validate_with_schema(value)
        return value

    @property
    def json_schema(self) -> JSONSchema:
        return any_of(
            string_schema(),
            number(),
            BOOL_SCHEMA
        )

    @property
    def is_abstract(self) -> bool:
        return False


String = ValueType.generate_subclass(str)
Integer = ValueType.generate_subclass(int)
Float = ValueType.generate_subclass(float)
Boolean = ValueType.generate_subclass(bool)
