from typing import Tuple

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, string_schema

from ufdl.jobtypes.base import UFDLJSONType


class String(UFDLJSONType[Tuple, str]):
    def parse_json_value(self, value: RawJSONElement) -> str:
        if not isinstance(value, str):
            raise ValueError("Value is not a string")
        return value

    def format_python_value_to_json(self, value: str) -> RawJSONElement:
        return value

    @property
    def json_schema(self) -> JSONSchema:
        return string_schema()

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple:
        return tuple()
