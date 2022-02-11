from typing import Tuple

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, IS_JSON_DEFINITION, IS_JSON_SCHEMA
from wai.json.schema.constants import DEFINITIONS_KEYWORD

from ...base import UFDLJSONType, UFDLType


class JSON(
    UFDLJSONType[
        tuple,
        RawJSONElement,
        RawJSONElement
    ]
):
    """
    Utility type for raw JSON values.
    """
    def parse_json_value(self, value: RawJSONElement) -> RawJSONElement:
        self.validate_with_schema(value)
        return value

    def format_python_value_to_json(self, value: RawJSONElement) -> RawJSONElement:
        self.validate_with_schema(value)
        return value

    @property
    def json_schema(self) -> JSONSchema:
        return {
            DEFINITIONS_KEYWORD: IS_JSON_DEFINITION,
            **IS_JSON_SCHEMA
        }

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return tuple()

    @property
    def is_abstract(self) -> bool:
        return False
