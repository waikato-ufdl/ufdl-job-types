from typing import Any, Type, Union

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, enum

from ..base import ServerResidentType, UFDLJSONType, UFDLType


class PK(UFDLJSONType[ServerResidentType[Union[UFDLType, None], Any], int]):
    def parse_json_value(self, value: RawJSONElement) -> int:
        if not isinstance(value, int):
            raise ValueError(f"Expected integer PK value; got {type(value)}")

        return value

    @property
    def json_schema(self) -> JSONSchema:
        return enum(
            *value['pk']
            for value in self.type_arg.list_all_values()
        )

    @classmethod
    def type_arg_expected_base_type(cls) -> Type[ServerResidentType]:
        return ServerResidentType
