from typing import Type

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, string_schema

from ufdl.jobtypes.base import NoTypeArg, UFDLJSONType


class String(UFDLJSONType[None, str]):
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
    def type_arg_expected_base_type(cls) -> Type[NoTypeArg]:
        return NoTypeArg
