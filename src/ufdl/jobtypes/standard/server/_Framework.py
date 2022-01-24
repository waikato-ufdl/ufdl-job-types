from typing import Dict, Tuple, Type

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, standard_object, string_schema

from ...base import ServerResidentType


class Framework(ServerResidentType[Tuple[str, str], RawJSONElement]):
    def server_table_name(self) -> str:
        return "Framework"

    def filter_rules(self) -> Dict[str, str]:
        return {
            "name": self.type_args[0],
            "version": self.type_args[1]
        }

    def parse_json_value(self, value: RawJSONElement) -> RawJSONElement:
        self.validate_with_schema(value)
        return value

    def format_python_value_to_json(self, value: RawJSONElement) -> RawJSONElement:
        return value

    @property
    def json_schema(self) -> JSONSchema:
        return standard_object(
            {"name": string_schema(max_length=32), "version": string_schema(max_length=32)}
        )

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[Type[str], Type[str]]:
        return str, str
