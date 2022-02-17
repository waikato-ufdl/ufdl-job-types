from typing import List, Optional, Tuple, Type, Union

from ufdl.json.core.filter import FilterExpression
from ufdl.json.core.filter.field import Exact
from wai.json.object import OptionallyPresent, StrictJSONObject
from wai.json.object.property import ConstantProperty, NumberProperty, StringProperty
from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema

from ...base import NamedServerType, String, UFDLType
from ...error import expect


class DomainInstance(StrictJSONObject['DomainInstance']):
    """
    Represents an instance of a deep-learning domain.
    """
    # The primary-key of the domain, if it was sent from the server
    pk: OptionallyPresent[int] = NumberProperty(integer_only=True, minimum=1, optional=True)

    # The name of the domain
    name: str = StringProperty(max_length=2)

    # The description of the domain
    description: str


class Domain(
    NamedServerType[
        Tuple[String],
        DomainInstance,
        DomainInstance
    ]
):
    def __init__(self, type_args: Union[str, Optional[Tuple[String]]] = None):
        if isinstance(type_args, str):
            type_args = (String.generate_subclass(type_args)(),)
        super().__init__(type_args)
        self._instance_class: Optional[Type[DomainInstance]] = None

    @property
    def instance_class(self):
        if self._instance_class is None:
            name_type = self.type_args[0].value()

            class SpecialisedDomainInstance(DomainInstance):
                description = (
                    ConstantProperty(value=name_type)
                    if isinstance(name_type, str) else
                    StringProperty(max_length=32)
                )

            self._instance_class = SpecialisedDomainInstance

        return self._instance_class

    def extract_name_from_json(self, value: RawJSONObject) -> str:
        return value['description']

    def name_filter(self, name: str) -> FilterExpression:
        return Exact(field='description', value=name)

    def server_table_name(self) -> str:
        return "domains"

    def filter_rules(self) -> List[FilterExpression]:
        rules = []
        name_type = self.type_args[0].value()
        if isinstance(name_type, str):
            rules.append(Exact(field="description", value=name_type))
        return rules

    def parse_json_value(self, value: RawJSONElement) -> DomainInstance:
        return self.instance_class.from_raw_json(value)

    def format_python_value_to_json(self, value: DomainInstance) -> RawJSONElement:
        expect(self.instance_class, value)
        return value.to_raw_json()

    @property
    def json_schema(self) -> JSONSchema:
        return self.instance_class.get_json_validation_schema()

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return String(),

    @property
    def is_abstract(self) -> bool:
        return False
