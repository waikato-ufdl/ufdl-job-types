from typing import Type

from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema

from ...base import ServerResidentType
from .._Domain import Domain


class Dataset(ServerResidentType[Domain, RawJSONObject]):
    def server_table_name(self) -> str:
        return f"{self.type_arg.extended_name}Dataset"

    def filter_rules(self) -> str:
        return ""

    def parse_json_value(self, value: RawJSONElement) -> RawJSONObject:
        return value

    @property
    def json_schema(self) -> JSONSchema:
        raise NotImplementedError(self.json_schema.__name__)

    @classmethod
    def type_arg_expected_base_type(cls) -> Type[Domain]:
        return Domain
