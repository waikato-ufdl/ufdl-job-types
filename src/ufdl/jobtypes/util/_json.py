import builtins

import jsonschema
from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema

from ..base import UFDLJSONType
from ._format import format_type
from ._simple import is_simple_type, parse_simple_json_value
from ._type import AnyUFDLType


def is_json_compatible(type: AnyUFDLType) -> bool:
    """
    Whether the given UFDL type has a JSON representation.

    :param type:
                The type to check.
    """
    return (
        is_simple_type(type)
        or isinstance(type, UFDLJSONType)
        or isinstance(type, builtins.type) and issubclass(type, UFDLJSONType)
    )


def parse_json_value(type: AnyUFDLType, value: RawJSONElement):
    if is_simple_type(type):
        return parse_simple_json_value(type, value)

    if isinstance(type, builtins.type) and issubclass(type, UFDLJSONType):
        type = type.type_base_equivalent()

    if isinstance(type, UFDLJSONType):
        return type.parse_json_value(value)

    raise ValueError(f"{format_type(type)} is not JSON-compatible")


def validate_with_schema(schema: JSONSchema, value: RawJSONElement):
    """
    Uses the type's schema to validate a value.

    :param schema:
                The schema to use for validation.
    :param value:
                The value to validate.
    """
    # Get the validator class
    validator_type = jsonschema.validators.validator_for(schema)

    # Check the schema is valid
    validator_type.check_schema(schema)

    # Create the instance
    validator = validator_type(schema)

    # Perform schema validation
    validator.validate(value)
