from typing import List, Optional, Tuple, overload

from ufdl.json.core.filter import FilterExpression
from ufdl.json.core.filter.field import Exact
from wai.json.object import OptionallyPresent, StrictJSONObject
from wai.json.object.property import NumberProperty, StringProperty
from wai.json.raw import RawJSONElement
from wai.json.schema import JSONSchema

from ...base import ServerResidentType, String, UFDLType
from ...error import expect


class FrameworkInstance(StrictJSONObject['FrameworkInstance']):
    """
    Represents an instance of a deep-learning framework
    """
    # The primary-key of the framework, if it was sent from the server
    pk: OptionallyPresent[int] = NumberProperty(integer_only=True, minimum=1, optional=True)

    # The name of the framework
    name: str = StringProperty(max_length=32)

    # The version of the framework
    version: str = StringProperty(max_length=32)


class Framework(
    ServerResidentType[
        Tuple[String, String],
        FrameworkInstance,
        FrameworkInstance
    ]
):
    @overload
    def __init__(self, name: str, version: str): ...
    @overload
    def __init__(self, type_args: Optional[Tuple[String, String]] = None): ...

    def __init__(self, *args):
        if len(args) == 0:
            super().__init__(None)
        elif len(args) == 1:
            super().__init__(args[0])
        else:
            super().__init__((String.generate_subclass(args[0])(), String.generate_subclass(args[1])()))

    def server_table_name(self) -> str:
        return "frameworks"

    def filter_rules(self) -> List[FilterExpression]:
        rules = []
        name_type, version_type = self.type_args
        if isinstance(name_type.value(), str):
            rules.append(Exact(field="name", value=name_type.value()))
        if isinstance(version_type.value(), str):
            rules.append(Exact(field="version", value=version_type.value()))
        return rules

    def parse_json_value(self, value: RawJSONElement) -> FrameworkInstance:
        return FrameworkInstance.from_raw_json(value)

    def format_python_value_to_json(self, value: FrameworkInstance) -> RawJSONElement:
        expect(FrameworkInstance, value)
        return value.to_raw_json()

    @property
    def json_schema(self) -> JSONSchema:
        return FrameworkInstance.get_json_validation_schema()

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return String(), String()

    @property
    def is_abstract(self) -> bool:
        return False
