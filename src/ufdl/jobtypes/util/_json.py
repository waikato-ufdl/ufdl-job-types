import builtins

import jsonschema
from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema

from ._simple import is_simple_type
from ._type import AnyUFDLType
from ..base import UFDLJSONType


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
