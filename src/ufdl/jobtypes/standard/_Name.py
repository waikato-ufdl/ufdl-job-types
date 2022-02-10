from typing import List, Tuple

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, enum

from ..base import FiniteJSONType, NamedServerType, UFDLType, PythonType


class Name(FiniteJSONType[Tuple[NamedServerType[tuple, PythonType]], PythonType]):
    def parse_json_value(self, value: RawJSONElement) -> PythonType:
        self.validate_with_schema(value)
        sub_type = self.type_args[0]
        return sub_type.parse_json_value(sub_type.get_json_value_by_name(value))

    def format_python_value_to_json(self, value: PythonType) -> RawJSONElement:
        sub_type = self.type_args[0]
        json_value = sub_type.format_python_value_to_json(value)
        return sub_type.extract_name_from_json(json_value)

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
