from typing import Tuple, Type, Union

from ufdl.json.core.filter import FilterSpec
from ufdl.json.core.filter.field import Exact
from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema, standard_object, number, string_schema

from ...base import NamedServerType, UFDLType
from ._Domain import Domain


class Dataset(
    NamedServerType[Tuple[Domain], RawJSONObject]
):
    def extract_name(self, value: RawJSONObject) -> str:
        return f"{value['name']} v{value['version']}"

    def server_table_name(self) -> str:
        domain_type = self.type_args[0]
        if isinstance(domain_type, Domain):
            description_type = domain_type.type_args[0]
            if isinstance(description_type, str):
                return f"{description_type.replace(' ', '')}Dataset"
        return "Dataset"

    def filter_rules(self) -> FilterSpec:
        rules = FilterSpec(expressions=[])
        domain_type = self.type_args[0]
        if isinstance(domain_type, Domain):
            description_type = domain_type.type_args[0]
            if isinstance(description_type, str):
                rules.expressions.append(Exact(field="domain.description", value=description_type))
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
                "name": string_schema(max_length=200),
                "version": number(minimum=1, integer_only=True)
            }
        )

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return Domain(),

    @property
    def is_abstract(self) -> bool:
        return False
