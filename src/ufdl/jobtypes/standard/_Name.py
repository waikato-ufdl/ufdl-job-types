from typing import List, Tuple

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, enum

from ..base import FiniteJSONType, NamedServerType, UFDLType


class Name(FiniteJSONType[Tuple[NamedServerType], str]):
    def parse_json_value(self, value: RawJSONElement) -> str:
        self.validate_with_schema(value)
        return value

    def format_python_value_to_json(self, value: str) -> RawJSONElement:
        self.validate_with_schema(value)
        return value

    def list_all_values(self) -> List[RawJSONElement]:
        sub_type = self.type_args[0]
        return list(
            sub_type.extract_name(value)
            for value in sub_type.list_all_values()
        )

    @property
    def json_schema(self) -> JSONSchema:
        return enum(*self.list_all_values())

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return NamedServerType(),

    @property
    def is_abstract(self) -> bool:
        return self.type_args[0].is_abstract
