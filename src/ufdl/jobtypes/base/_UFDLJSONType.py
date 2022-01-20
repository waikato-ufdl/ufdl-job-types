import json
from abc import abstractmethod

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema

from ._PythonType import PythonType
from ._UFDLBinaryType import UFDLBinaryType
from ._UFDLType import TypeArgType


class UFDLJSONType(
    UFDLBinaryType[TypeArgType, PythonType],
    abstract=True
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

    @property
    @abstractmethod
    def json_schema(self) -> JSONSchema:
        """
        The schema used by this type to validate input data.
        """
        raise NotImplementedError(self.json_schema.__name__)
