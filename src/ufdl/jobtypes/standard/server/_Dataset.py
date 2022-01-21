from typing import Dict, Tuple, Type

from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema

from ...base import ServerResidentType
from ._Domain import Domain


class Dataset(ServerResidentType[Tuple[Domain], RawJSONObject]):
    def server_table_name(self) -> str:
        return f"{self.type_args[0].extended_name}Dataset"

    def filter_rules(self) -> Dict[str, str]:
        return {}

    def parse_json_value(self, value: RawJSONElement) -> RawJSONObject:
        self.validate_with_schema(value)
        return value

    def format_python_value_to_json(self, value: RawJSONObject) -> RawJSONElement:
        raise NotImplementedError(self.format_python_value_to_json.__name__)

    @property
    def json_schema(self) -> JSONSchema:
        raise NotImplementedError(self.json_schema.__name__)

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[Type[Domain]]:
        return Domain,
