from typing import List, Tuple

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, NULL_SCHEMA

from ...base import FiniteJSONType, UFDLType
from ...error import expect


class Nothing(
    FiniteJSONType[
        tuple,
        None,
        None
    ]
):
    """
    Utility type which expects a null value. Useful in combination with other types
    to provide the option to not use something.
    """
    def parse_json_value(self, value: RawJSONElement) -> None:
        self.validate_with_schema(value)
        return value

    def format_python_value_to_json(self, value: None) -> RawJSONElement:
        expect(None, value)
        return value

    def list_all_json_values(self) -> List[RawJSONElement]:
        return [None]

    @property
    def json_schema(self) -> JSONSchema:
        return NULL_SCHEMA

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return tuple()

    @property
    def is_abstract(self) -> bool:
        return False
