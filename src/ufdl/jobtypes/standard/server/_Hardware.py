from typing import List, Tuple

from ufdl.json.core.filter import FilterExpression
from ufdl.json.core.filter.field import Exact
from wai.json.object import OptionallyPresent, StrictJSONObject
from wai.json.object.property import NumberProperty, StringProperty
from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema

from ...base import NamedServerType, String, UFDLType
from ...error import expect


class HardwareInstance(StrictJSONObject['HardwareInstance']):
    """
    Represents an instance of a hardware specification.
    """
    # The primary-key of the hardware spec, if it was sent from the server
    pk: OptionallyPresent[int] = NumberProperty(integer_only=True, minimum=1, optional=True)

    # The name of the hardware generation
    generation: str = StringProperty()

    # The minimum compute capability of the generation of hardware
    min_compute_capability: float = NumberProperty()

    # The maximum compute capability of the generation of hardware
    max_compute_capability: float = NumberProperty()


class Hardware(
    NamedServerType[
        Tuple[String],
        HardwareInstance,
        HardwareInstance
    ]
):
    def extract_name_from_json(self, value: RawJSONObject) -> str:
        return value['generation']

    def name_filter(self, name: str) -> FilterExpression:
        return Exact(field='generation', value=name)

    def server_table_name(self) -> str:
        return "hardware"

    def filter_rules(self) -> List[FilterExpression]:
        return []

    def parse_json_value(self, value: RawJSONElement) -> HardwareInstance:
        return HardwareInstance.from_raw_json(value)

    def format_python_value_to_json(self, value: HardwareInstance) -> RawJSONElement:
        expect(HardwareInstance, value)
        return value.to_raw_json()

    @property
    def json_schema(self) -> JSONSchema:
        return HardwareInstance.get_json_validation_schema()

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return tuple()

    @property
    def is_abstract(self) -> bool:
        return False
