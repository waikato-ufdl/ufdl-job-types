import json
from abc import abstractmethod

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema

from ._UFDLType import UFDLType, TypeArgsType, PythonType


class UFDLJSONType(
    UFDLType[TypeArgsType, PythonType],
    abstract=True
):
    """
    TODO
    """
    def parse_binary_value(self, value: bytes) -> PythonType:
        return self.parse_json_value(json.loads(value.decode("UTF-8")))

    @abstractmethod
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

    @abstractmethod
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
    @abstractmethod
    def json_schema(self) -> JSONSchema:
        """
        The schema used by this type to validate input data.
        """
        raise NotImplementedError(self.json_schema.__name__)

    def validate_with_schema(self, value: RawJSONElement):
        """
        Uses the type's schema to validate a value.

        :param schema:
                    The schema to use for validation.
        :param value:
                    The value to validate.
        """
        from ..util import validate_with_schema
        validate_with_schema(self.json_schema, value)
