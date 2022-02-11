from typing import List, Tuple

from ufdl.json.core.filter import FilterExpression
from ufdl.json.core.filter.field import Exact
from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema, standard_object, number, string_schema

from ...base import NamedServerType, UFDLType
from ...util import parse_v_name
from ._Domain import Domain
from ._Framework import Framework


class DockerImage(
    NamedServerType[
        Tuple[Domain, Framework],
        RawJSONObject,
        RawJSONObject
    ]
):
    def name_filter(self, name: str) -> FilterExpression:
        name, version = parse_v_name(name)
        return Exact(field="name", value=name) & Exact(field="version", value=version)

    def extract_name_from_json(self, value: RawJSONObject) -> str:
        return f"{value['name']} v{value['version']}"

    def server_table_name(self) -> str:
        return "DockerImage"

    def filter_rules(self) -> List[FilterExpression]:
        rules = []
        domain_type, framework_type = self.type_args
        if isinstance(domain_type, Domain):
            description_type = domain_type.type_args[0].value()
            if isinstance(description_type, str):
                rules.append(Exact(field="domain.description", value=description_type))
        if isinstance(framework_type, Framework):
            name_type, version_type = framework_type.type_args
            if isinstance(name_type.value(), str):
                rules.append(Exact(field="framework.name", value=name_type.value()))
            if isinstance(version_type.value(), str):
                rules.append(Exact(field="framework.version", value=version_type.value()))

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
                "name": string_schema(max_length=64),
                "version": string_schema(max_length=32)
            }
        )

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return Domain(), Framework()

    @property
    def is_abstract(self) -> bool:
        return False
