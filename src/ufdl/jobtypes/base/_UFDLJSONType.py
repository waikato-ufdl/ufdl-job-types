import json
from abc import abstractmethod

import jsonschema
from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema

from ._UFDLType import UFDLType, TypeArgsType, PythonType


class UFDLJSONType(
    UFDLType[TypeArgsType, PythonType]
):
    """
    TODO
    """
    def parse_binary_value(self, value: bytes) -> PythonType:
        return self.parse_json_value(json.loads(value.decode("UTF-8")))

    def parse_json_value(self, value: RawJSONElement) -> PythonType:
        """
        Parses a raw value supplied as JSON into the Python-type.

        :param value:
                    The value to parse, as JSON.
        :return:
                    The value parsed into Python.
        """
        raise NotImplementedError(self.parse_json_value.__name__)

    def format_python_value(self, value: PythonType) -> bytes:
        return json.dumps(self.format_python_value_to_json(value)).encode("UTF-8")

    def format_python_value_to_json(self, value: PythonType) -> RawJSONElement:
        """
        Formats a Python value into JSON.

        :param value:
                    The value to format.
        :return:
                    The raw JSON representation of the value.
        """
        raise NotImplementedError(self.format_python_value_to_json.__name__)

    @property
    def json_schema(self) -> JSONSchema:
        """
        The schema used by this type to validate input data.
        """
        raise NotImplementedError(self.json_schema.__name__)

    def validate_with_schema(self, value: RawJSONElement):
        """
        Uses the type's schema to validate a value.

        :param value:
                    The value to validate.
        """
        # Get our schema
        schema = self.json_schema

        # Get the validator class
        validator_type = jsonschema.validators.validator_for(schema)

        # Check the schema is valid
        validator_type.check_schema(schema)

        # Create the instance
        validator = validator_type(schema)

        # Perform schema validation
        validator.validate(value)
