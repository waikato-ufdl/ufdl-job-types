from typing import List, Tuple

from ufdl.json.core.filter import FilterExpression
from ufdl.json.core.filter.field import Exact
from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema, enum

from ..base import InputType, OutputType, UFDLType, ServerResidentType
from ..error import expect
from ..initialise import download_function
from ..util import read_all


class JobOutput(
    ServerResidentType[
        Tuple[UFDLType[Tuple[UFDLType, ...], InputType, OutputType]],
        InputType,
        int
    ]
):
    def server_table_name(self) -> str:
        return "job-outputs"

    def filter_rules(self) -> List[FilterExpression]:
        return [
            Exact(field="type", value=str(self.type_args[0]))
        ]

    def parse_json_value(self, value: RawJSONElement) -> InputType:
        self.validate_with_schema(value)
        downloaded_job_output_data = download_function(self.server_table_name(), value)
        if not isinstance(downloaded_job_output_data, bytes):
            downloaded_job_output_data = read_all(downloaded_job_output_data)
        return self.type_args[0].parse_binary_value(downloaded_job_output_data)

    def format_python_value_to_json(self, value: int) -> RawJSONElement:
        expect(int, value)
        return value

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
