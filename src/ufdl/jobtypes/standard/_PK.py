from typing import Tuple, Type

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, enum

from ..base import ServerResidentType, UFDLJSONType, UFDLType


class PK(UFDLJSONType[Tuple[ServerResidentType], int]):
    def parse_json_value(self, value: RawJSONElement) -> int:
        if not isinstance(value, int):
            raise ValueError(f"Expected integer PK value; got {type(value)}")

        return value

    def format_python_value_to_json(self, value: int) -> RawJSONElement:
        return value

    @property
    def json_schema(self) -> JSONSchema:
        return enum(
            *(
                value['pk']
                for value in self.type_args[0].list_all_values()
            )
        )

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return ServerResidentType(),
