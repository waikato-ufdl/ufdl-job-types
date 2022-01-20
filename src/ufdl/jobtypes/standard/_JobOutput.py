from typing import Dict, Type

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, enum

from ..base import PythonType, UFDLBinaryType, ServerResidentType
from ..initialise import download_function
from ..util import format_type_or_type_class


class JobOutput(ServerResidentType[UFDLBinaryType[PythonType], PythonType]):
    def server_table_name(self) -> str:
        return "JobOutput"

    def filter_rules(self) -> Dict[str, str]:
        return {'type': format_type_or_type_class(self.type_arg)}

    def parse_json_value(self, value: RawJSONElement) -> PythonType:
        if not isinstance(value, int):
            raise ValueError(f"Expected integer PK of a job output; got {type(value)}")

        return self.type_arg.parse_binary_value(
            download_function(self.server_table_name(), value)
        )

    @property
    def json_schema(self) -> JSONSchema:
        return enum(
            *value['pk']
            for value in self.list_all_values()
        )

    @classmethod
    def type_arg_expected_base_type(cls) -> Type[UFDLBinaryType]:
        return UFDLBinaryType
