from typing import Tuple, Type, Union

from ufdl.json.core.filter import FilterSpec
from ufdl.json.core.filter.field import Exact
from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema

from ufdl.jobtypes.base import NamedServerType
from ufdl.jobtypes.standard.server import Domain, Framework


class DockerImage(
    NamedServerType[
        Tuple[Union[Domain, Type[Domain]], Union[Framework, Type[Framework]]],
        RawJSONObject
    ]
):
    def extract_name(self, value: RawJSONObject) -> str:
        return f"{value['name']} v{value['version']}"

    def server_table_name(self) -> str:
        return "DockerImage"

    def filter_rules(self) -> FilterSpec:
        rules = FilterSpec(expressions=[])
        domain_type, framework_type = self.type_args
        if isinstance(domain_type, Domain):
            name_type, description_type = domain_type.type_args
            if isinstance(name_type, str):
                rules.expressions.append(Exact(field="domain.name", value=name_type))
            if isinstance(description_type, str):
                rules.expressions.append(Exact(field="domain.description", value=description_type))
        if isinstance(framework_type, Framework):
            name_type, version_type = framework_type.type_args
            if isinstance(name_type, str):
                rules.expressions.append(Exact(field="framework.name", value=name_type))
            if isinstance(version_type, str):
                rules.expressions.append(Exact(field="framework.version", value=version_type))

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
    def type_params_expected_base_types(cls) -> Tuple[Type[Domain], Type[Framework]]:
        return Domain, Framework
