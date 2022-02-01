from typing import Tuple

from ufdl.json.core.filter import FilterSpec
from ufdl.json.core.filter.field import Exact
from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema, standard_object, string_schema, number

from ...base import ServerResidentType, String, UFDLType


class Framework(ServerResidentType[Tuple[String, String], RawJSONObject]):
    def server_table_name(self) -> str:
        return "Framework"

    def filter_rules(self) -> FilterSpec:
        rules = FilterSpec(expressions=[])
        name_type, version_type = self.type_args
        if isinstance(name_type.value(), str):
            rules.expressions.append(Exact(field="name", value=name_type.value()))
        if isinstance(version_type.value(), str):
            rules.expressions.append(Exact(field="version", value=version_type.value()))
        return rules

    def parse_json_value(self, value: RawJSONElement) -> RawJSONObject:
        self.validate_with_schema(value)
        return value

    def format_python_value_to_json(self, value: RawJSONObject) -> RawJSONElement:
        self.validate_with_schema(value)
        return value

    @property
    def json_schema(self) -> JSONSchema:
        return standard_object(
            {
                "pk": number(minimum=1, integer_only=True),
                "name": string_schema(max_length=32),
                "version": string_schema(max_length=32)
            }
        )

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return String(), String()

    @property
    def is_abstract(self) -> bool:
        return False
