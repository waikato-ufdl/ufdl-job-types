from typing import Dict, Tuple, Type

from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema

from ...base import ServerResidentType


class Domain(ServerResidentType[Tuple[str], str]):
    def server_table_name(self) -> str:
        return "DataDomain"

    def filter_rules(self) -> Dict[str, str]:
        return {"name": self.type_args[0].lower()}

    @property
    def json_schema(self) -> JSONSchema:
        raise NotImplementedError(self.json_schema.__name__)

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[Type[str]]:
        return str,
