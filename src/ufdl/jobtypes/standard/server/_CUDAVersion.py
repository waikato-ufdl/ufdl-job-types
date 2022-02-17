from typing import List, Optional, Tuple, Union

from ufdl.json.core.filter import FilterExpression
from ufdl.json.core.filter.field import Exact
from wai.json.object import OptionallyPresent, StrictJSONObject
from wai.json.object.property import NumberProperty, StringProperty
from wai.json.raw import RawJSONElement, RawJSONObject
from wai.json.schema import JSONSchema

from ...base import NamedServerType, String, UFDLType
from ...error import expect


class CUDAVersionInstance(StrictJSONObject['CUDAVersionInstance']):
    """
    Represents an instance of a CUDA version.
    """
    # The primary-key of the CUDA version, if it was sent from the server
    pk: OptionallyPresent[int] = NumberProperty(integer_only=True, minimum=1, optional=True)

    # The CUDA version number
    version: float = NumberProperty()

    # The full CUDA version string
    full_version: str = StringProperty(max_length=16)

    # The minimum NVidia driver version that supports this CUDA version
    min_driver_version: str = StringProperty(max_length=16)


class CUDAVersion(
    NamedServerType[
        Tuple[String],
        CUDAVersionInstance,
        CUDAVersionInstance
    ]
):
    def extract_name_from_json(self, value: RawJSONObject) -> str:
        return value['full_version']

    def name_filter(self, name: str) -> FilterExpression:
        return Exact(field='full_version', value=name)

    def server_table_name(self) -> str:
        return "cuda"

    def filter_rules(self) -> List[FilterExpression]:
        return []

    def parse_json_value(self, value: RawJSONElement) -> CUDAVersionInstance:
        return CUDAVersionInstance.from_raw_json(value)

    def format_python_value_to_json(self, value: CUDAVersionInstance) -> RawJSONElement:
        expect(CUDAVersionInstance, value)
        return value.to_raw_json()

    @property
    def json_schema(self) -> JSONSchema:
        return CUDAVersionInstance.get_json_validation_schema()

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return tuple()

    @property
    def is_abstract(self) -> bool:
        return False
