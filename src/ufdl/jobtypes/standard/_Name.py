from typing import Tuple, Type

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, enum

from ..base import UFDLJSONType, NamedServerType, UFDLType


class Name(UFDLJSONType[Tuple[NamedServerType], str]):
    def parse_json_value(self, value: RawJSONElement) -> str:
        if not isinstance(value, str):
            raise ValueError("Not a string")
        return value

    def format_python_value_to_json(self, value: str) -> RawJSONElement:
        return value

    @property
    def json_schema(self) -> JSONSchema:
        sub_type = self.type_args[0]
        return enum(
            *(
                sub_type.extract_name(value)
                for value in sub_type.list_all_values()
            )
        )

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return NamedServerType(),

    @property
    def is_abstract(self) -> bool:
        return self.type_args[0].is_abstract
