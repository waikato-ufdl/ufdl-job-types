from typing import Tuple

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, number

from ufdl.jobtypes.base import UFDLJSONType


class Integer(UFDLJSONType[Tuple, int]):
    """
    TODO
    """
    def parse_json_value(self, value: RawJSONElement) -> int:
        if not isinstance(value, int):
            raise ValueError(f"Expected int, got {type(value)}")
        return value

    def format_python_value_to_json(self, value: int) -> RawJSONElement:
        return value

    @property
    def json_schema(self) -> JSONSchema:
        return number(integer_only=True)

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple:
        return tuple()
