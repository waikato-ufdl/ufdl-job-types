from typing import Dict, Type

from wai.json.raw import RawJSONObject
from wai.json.schema import JSONSchema

from ...base import NoTypeArg, ServerResidentType


class Domain(ServerResidentType[str, str]):
    def server_table_name(self) -> str:
        return "DataDomain"

    def filter_rules(self) -> Dict[str, str]:
        return {"name": self.type_arg.lower()}

    def parse_json_value(self, value: RawJSONObject) -> RawJSONObject:
        return value

    @property
    def json_schema(self) -> JSONSchema:
        raise NotImplementedError(self.json_schema.__name__)

    @classmethod
    def type_arg_expected_base_type(cls) -> Type[str]:
        return str
