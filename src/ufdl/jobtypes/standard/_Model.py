from typing import Tuple, Type

from ufdl.jobtypes.base import UFDLBinaryType
from ufdl.jobtypes.standard.server import Domain


class Model(UFDLBinaryType[Tuple[Domain], bytes]):
    def parse_binary_value(self, value: bytes) -> bytes:
        return value

    def format_python_value(self, value: bytes) -> bytes:
        return value

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[Type[Domain]]:
        return Domain,
