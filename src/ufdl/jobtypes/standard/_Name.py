from typing import List, Tuple

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, enum

from ..base import FiniteJSONType, NamedServerType, UFDLType, InputType, OutputType
from ..error import expect


class Name(
    FiniteJSONType[
        Tuple[NamedServerType[tuple, InputType, OutputType]],
        InputType,
        str
    ]
):
    def parse_json_value(self, value: RawJSONElement) -> InputType:
        expect(str, value)
        sub_type = self.type_args[0]
        return sub_type.get_python_value_by_name(value)

    def format_python_value_to_json(self, value: str) -> RawJSONElement:
        self.validate_with_schema(value)
        return value

    def list_all_json_values(self) -> List[RawJSONElement]:
        sub_type = self.type_args[0]
        return list(
            sub_type.extract_name_from_json(value)
            for value in sub_type.list_all_json_values()
        )

    @property
    def json_schema(self) -> JSONSchema:
        return enum(*self.list_all_json_values())

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return NamedServerType(),

    @property
    def is_abstract(self) -> bool:
        return self.type_args[0].is_abstract
