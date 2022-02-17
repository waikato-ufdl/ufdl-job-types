from typing import List, Optional, Tuple, Type, overload

from ufdl.json.core.filter import FilterExpression
from ufdl.json.core.filter.field import Exact

from wai.json.object import OptionallyPresent, StrictJSONObject
from wai.json.object.property import (
    BoolProperty,
    NumberProperty,
    StringProperty,
    ConstantProperty,
    OneOfProperty
)
from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema

from ...base import NamedServerType, UFDLType
from ._Domain import Domain
from ._Framework import Framework, FrameworkInstance
from ...error import expect


class PretrainedModelInstance(StrictJSONObject['PretrainedModelInstance']):
    """
    Instance-representation of a pre-trained model.
    """
    # The primary-key of the model, if it was sent by the server
    pk: OptionallyPresent[int] = NumberProperty(integer_only=True, minimum=1, optional=True)

    url: str = StringProperty()

    name: OptionallyPresent[str] = StringProperty(optional=True)

    description: OptionallyPresent[str] = StringProperty(optional=True)

    # The framework of the model
    framework: FrameworkInstance = FrameworkInstance.as_property()

    domain: str = StringProperty()

    licence: OptionallyPresent[str] = StringProperty()

    data: bool = BoolProperty(optional=True, default=False)

    metadata: OptionallyPresent[str] = StringProperty(optional=True)

    creator: OptionallyPresent[Optional[int]] = OneOfProperty(
        sub_properties=(
            NumberProperty(integer_only=True, minimum=1),
            ConstantProperty(value=None)
        ),
        optional=True
    )

    creation_time: OptionallyPresent[str] = StringProperty(optional=True)

    deletion_time: OptionallyPresent[Optional[str]] = OneOfProperty(
        sub_properties=(
            StringProperty(),
            ConstantProperty(value=None)
        ),
        optional=True
    )


class PretrainedModel(
    NamedServerType[
        Tuple[Domain, Framework],
        PretrainedModelInstance,
        PretrainedModelInstance
    ]
):
    @overload
    def __init__(self, domain_type: Domain, framework_type: Framework): ...
    @overload
    def __init__(self, type_args: Optional[Tuple[Domain, Framework]] = None): ...

    def __init__(self, *args):
        if len(args) == 2:
            args = args,
        super().__init__(*args)
        self._instance_class: Optional[Type[PretrainedModelInstance]] = None

    @property
    def instance_class(self):
        if self._instance_class is None:
            domain_type = self.type_args[0]
            framework_type = self.type_args[1]

            class SpecialisedPretrainedModelInstance(PretrainedModelInstance):
                framework = framework_type.instance_class.as_property()
                domain = domain_type.instance_class.description

            self._instance_class = SpecialisedPretrainedModelInstance

        return self._instance_class

    def name_filter(self, name: str) -> FilterExpression:
        return Exact(field="name", value=name)

    def extract_name_from_json(self, value: RawJSONObject) -> str:
        return value['name']

    def server_table_name(self) -> str:
        return "pretrained-models"

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

    def parse_json_value(self, value: RawJSONElement) -> PretrainedModelInstance:
        return self.instance_class.from_raw_json(value)

    def format_python_value_to_json(self, value: PretrainedModelInstance) -> RawJSONElement:
        expect(self.instance_class, value)
        return value.to_raw_json()

    @property
    def json_schema(self) -> JSONSchema:
        return self.instance_class.get_json_validation_schema()

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return Domain(), Framework()

    @property
    def is_abstract(self) -> bool:
        return False
