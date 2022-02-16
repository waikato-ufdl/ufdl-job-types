from typing import List, Optional, Tuple, Union

from ufdl.json.core.filter import FilterExpression
from ufdl.json.core.filter.field import Exact
from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema, standard_object, number, string_schema

from ...base import NamedServerType, String, UFDLType


class Domain(
    NamedServerType[
        Tuple[String],
        RawJSONObject,
        RawJSONObject
    ]
):
    def __init__(self, type_args: Union[str, Optional[Tuple[String]]] = None):
        if isinstance(type_args, str):
            type_args = (String.generate_subclass(type_args),)
        super().__init__(type_args)

    def extract_name_from_json(self, value: RawJSONObject) -> str:
        return value['name']

    def name_filter(self, name: str) -> FilterExpression:
        return Exact(field='name', value=name)

    def server_table_name(self) -> str:
        return "DataDomain"

    def filter_rules(self) -> List[FilterExpression]:
        rules = []
        name_type = self.type_args[0]
        if isinstance(name_type, str):
            rules.append(Exact(field="description", value=name_type.lower()))
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
                "name": string_schema(max_length=2),
                "description": string_schema(max_length=32)
            }
        )

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return String(),

    @property
    def is_abstract(self) -> bool:
        return False
