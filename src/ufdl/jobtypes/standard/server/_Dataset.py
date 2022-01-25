from typing import Dict, Tuple, Type, Union

from ufdl.json.core.filter import FilterSpec
from ufdl.json.core.filter.field import Exact
from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema

from ...base import ServerResidentType
from ._Domain import Domain


class Dataset(ServerResidentType[Tuple[Union[Domain, Type[Domain]]], RawJSONObject]):
    def server_table_name(self) -> str:
        domain_type = self.type_args[0]
        if isinstance(domain_type, Domain):
            description_type = domain_type.type_args[1]
            if isinstance(description_type, str):
                description = "".join(description_type.split(" "))
                return f"{description}Dataset"
        return "Dataset"

    def filter_rules(self) -> FilterSpec:
        rules = FilterSpec(expressions=[])
        domain_type = self.type_args[0]
        if isinstance(domain_type, Domain):
            name_type, description_type = domain_type.type_args
            if isinstance(name_type, str):
                rules.expressions.append(Exact(field="domain.name", value=name_type))
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
        raise NotImplementedError(self.json_schema.__name__)

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[Type[Domain]]:
        return Domain,
