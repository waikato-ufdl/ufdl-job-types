from typing import List, Tuple

from ufdl.json.core.filter.field import Exact

from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, enum

from ..base import InputType, OutputType, ServerResidentType, FiniteJSONType, UFDLType
from ..error import expect


class PK(
    FiniteJSONType[
        Tuple[ServerResidentType[tuple, InputType, OutputType]],
        InputType,
        int
    ]
):
    def list_all_json_values(self) -> List[RawJSONElement]:
        return [
            value['pk']
            for value in self.type_args[0].list_all_json_values()
        ]

    def parse_json_value(self, value: RawJSONElement) -> InputType:
        expect(int, value)
        sub_type = self.type_args[0]
        results = sub_type.get_filtered_list_of_json_values(Exact(field="pk", value=value))
        if len(results) != 1:
            raise Exception(f"Couldn't get unique value with PK {value} from server")
        return sub_type.parse_json_value(value[0])

    def format_python_value_to_json(self, value: int) -> RawJSONElement:
        self.validate_with_schema(value)
        return value

    @property
    def json_schema(self) -> JSONSchema:
        return enum(*self.list_all_json_values())

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return ServerResidentType(),

    @property
    def is_abstract(self) -> bool:
        return self.type_args[0].is_abstract
