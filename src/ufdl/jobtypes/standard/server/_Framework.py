from typing import List, Optional, Tuple, Type, overload

from ufdl.json.core.filter import FilterExpression
from ufdl.json.core.filter.field import Exact
from wai.json.object import OptionallyPresent, StrictJSONObject
from wai.json.object.property import ConstantProperty, NumberProperty, StringProperty
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
    name: str

    # The version of the framework
    version: str


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
        self._instance_class: Optional[Type[FrameworkInstance]] = None

    @property
    def instance_class(self):
        if self._instance_class is None:
            name_type = self.type_args[0].value()
            version_type = self.type_args[1].value()

            class SpecialisedFrameworkInstance(FrameworkInstance):
                name = (
                    ConstantProperty(value=name_type)
                    if isinstance(name_type, str) else
                    StringProperty(max_length=32)
                )
                version = (
                    ConstantProperty(value=version_type)
                    if isinstance(version_type, str) else
                    StringProperty(max_length=32)
                )

            self._instance_class = SpecialisedFrameworkInstance
        return self._instance_class

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
        return self.instance_class.from_raw_json(value)

    def format_python_value_to_json(self, value: FrameworkInstance) -> RawJSONElement:
        expect(self.instance_class, value)
        return value.to_raw_json()

    @property
    def json_schema(self) -> JSONSchema:
        return self.instance_class.get_json_validation_schema()

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return String(), String()

    @property
    def is_abstract(self) -> bool:
        return False
