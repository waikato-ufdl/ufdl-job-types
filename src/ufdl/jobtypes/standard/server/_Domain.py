from typing import Dict, Tuple, Type

from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema

from ...base import ServerResidentType
from ..._type import StrType


class Domain(ServerResidentType[Tuple[StrType, StrType], RawJSONObject]):
    def server_table_name(self) -> str:
        return "DataDomain"

    def filter_rules(self) -> Dict[str, str]:
        rules = {}
        name_type = self.type_args[0]
        description_type = self.type_args[1]
        if isinstance(name_type, str):
            rules["name"] = name_type.lower()
        if isinstance(description_type, str):
            rules["description"] = description_type
        return rules

    def parse_json_value(self, value: RawJSONElement) -> RawJSONObject:
        self.validate_with_schema(value)
        return value

    def format_python_value_to_json(self, value: RawJSONObject) -> RawJSONElement:
        self.validate_with_schema(value)
        return value

    @property
    def json_schema(self) -> JSONSchema:
        raise NotImplementedError(self.json_schema.__name__)

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[Type[str], Type[str]]:
        return str, str
