from typing import Tuple

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, BOOL_SCHEMA

from ufdl.jobtypes.base import UFDLJSONType


class Boolean(UFDLJSONType[Tuple, bool]):
    """
    TODO
    """
    def parse_json_value(self, value: RawJSONElement) -> bool:
        if not isinstance(value, bool):
            raise ValueError(f"Expected bool, got {type(value)}")
        return value

    def format_python_value_to_json(self, value: bool) -> RawJSONElement:
        return value

    @property
    def json_schema(self) -> JSONSchema:
        return BOOL_SCHEMA

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple:
        return tuple()
