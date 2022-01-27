from typing import Tuple, Type

from ufdl.json.core.filter import FilterSpec
from ufdl.json.core.filter.field import Exact
from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema

from ...base import ServerResidentType
from ...util import StrType


class Domain(ServerResidentType[Tuple[StrType], RawJSONObject]):
    def server_table_name(self) -> str:
        return "DataDomain"

    def filter_rules(self) -> FilterSpec:
        rules = FilterSpec(expressions=[])
        name_type = self.type_args[0]
        if isinstance(name_type, str):
            rules.expressions.append(Exact(field="description", value=name_type.lower()))
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
    def type_params_expected_base_types(cls) -> Tuple[Type[str]]:
        return str,
