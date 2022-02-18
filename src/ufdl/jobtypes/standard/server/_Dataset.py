from typing import List, Optional, Tuple, Type

from ufdl.json.core.filter import FilterExpression
from ufdl.json.core.filter.field import Exact
from wai.json.object import JSONObject
from wai.json.object.property import ConstantProperty, NumberProperty, StringProperty
from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema, standard_object, number, string_schema

from ...base import NamedServerType, UFDLType
from ...error import expect
from ...util import parse_v_name
from ._Domain import Domain


class DatasetInstance(JSONObject['DatasetInstance']):
    """
    A value of the Dataset type.

    TODO: Remaining fields.
    """
    pk: int = NumberProperty(minimum=1, integer_only=True)

    name: str = StringProperty()

    version: int = NumberProperty(minimum=1, integer_only=True)

    domain: str


class Dataset(
    NamedServerType[
        Tuple[Domain],
        DatasetInstance,
        DatasetInstance
    ]
):
    def __init__(self, type_args: Optional[Tuple[Domain]] = None):
        super().__init__(type_args)
        self._instance_class: Optional[Type[DatasetInstance]] = None

    @property
    def instance_class(self):
        if self._instance_class is None:
            domain_type = self.type_args[0].type_args[0].value()

            class SpecialisedDatasetInstance(DatasetInstance):
                domain = (
                    ConstantProperty(value=domain_type)
                    if isinstance(domain_type, str) else
                    StringProperty(max_length=32)
                )

            self._instance_class = SpecialisedDatasetInstance

        return self._instance_class

    def name_filter(self, name: str) -> FilterExpression:
        name, version = parse_v_name(name)
        return Exact(field="name", value=name) & Exact(field="version", value=int(version))

    def extract_name_from_json(self, value: RawJSONObject) -> str:
        return f"{value['name']} v{value['version']}"

    def server_table_name(self) -> str:
        return "datasets"

    def filter_rules(self) -> List[FilterExpression]:
        rules = []
        domain_type = self.type_args[0]
        if isinstance(domain_type, Domain):
            description_type = domain_type.type_args[0].value()
            if isinstance(description_type, str):
                rules.append(Exact(field="domain.description", value=description_type))
        return rules

    def parse_json_value(self, value: RawJSONElement) -> DatasetInstance:
        return self.instance_class.from_raw_json(value)

    def format_python_value_to_json(self, value: DatasetInstance) -> RawJSONElement:
        expect(DatasetInstance, value)
        return value.to_raw_json()

    @property
    def json_schema(self) -> JSONSchema:
        return self.instance_class.get_json_validation_schema()

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return Domain(),

    @property
    def is_abstract(self) -> bool:
        return False
