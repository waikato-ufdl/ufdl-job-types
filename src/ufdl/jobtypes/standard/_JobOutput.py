from typing import List, Tuple

from ufdl.json.core.filter import FilterExpression
from ufdl.json.core.filter.field import Exact
from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, enum

from ..base import PythonType, UFDLType, ServerResidentType
from ..initialise import download_function


class JobOutput(
    ServerResidentType[
        Tuple[UFDLType[Tuple[UFDLType, ...], PythonType]],
        PythonType
    ]
):
    def server_table_name(self) -> str:
        return "JobOutput"

    def filter_rules(self) -> List[FilterExpression]:
        return [
            Exact(field="type", value=str(self.type_args[0]))
        ]

    def parse_json_value(self, value: RawJSONElement) -> PythonType:
        if not isinstance(value, int):
            raise ValueError(f"Expected integer PK of a job output; got {type(value)}")

        return self.type_args[0].parse_binary_value(
            download_function(self.server_table_name(), value)
        )

    def format_python_value_to_json(self, value: PythonType) -> RawJSONElement:
        raise NotImplementedError(self.format_python_value_to_json.__name__)

    @property
    def json_schema(self) -> JSONSchema:
        return enum(
            *(
                value['pk']
                for value in self.list_all_json_values()
            )
        )

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return UFDLType(),

    @property
    def is_abstract(self) -> bool:
        return self.type_args[0].is_abstract
