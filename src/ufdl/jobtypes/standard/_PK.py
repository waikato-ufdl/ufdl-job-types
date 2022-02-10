from typing import List, Tuple

from ufdl.json.core.filter.field import Exact
from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, enum

from ..base import PythonType, ServerResidentType, FiniteJSONType, UFDLType


class PK(FiniteJSONType[Tuple[ServerResidentType[tuple, PythonType]], PythonType]):
    def list_all_json_values(self) -> List[RawJSONElement]:
        return [
            value['pk']
            for value in self.type_args[0].list_all_json_values()
        ]

    def parse_json_value(self, value: RawJSONElement) -> PythonType:
        self.validate_with_schema(value)
        results = self.type_args[0].get_filtered_list_of_json_values(Exact(field="pk", value=value))
        if len(results) != 1:
            raise Exception(f"Couldn't get unique value with PK {value} from server")
        return value[0]

    def format_python_value_to_json(self, value: PythonType) -> RawJSONElement:
        sub_type = self.type_args[0]
        pk = sub_type.format_python_value_to_json(value)['pk']
        self.validate_with_schema(pk)
        return pk

    @property
    def json_schema(self) -> JSONSchema:
        return enum(*self.list_all_json_values())

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return ServerResidentType(),

    @property
    def is_abstract(self) -> bool:
        return self.type_args[0].is_abstract
