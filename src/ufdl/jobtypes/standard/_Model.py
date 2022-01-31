from typing import Tuple, Type, Union

from ..base import UFDLType
from .server import Domain, Framework


class Model(
    UFDLType[
        Tuple[Domain, Framework],
        bytes
    ]
):
    def parse_binary_value(self, value: bytes) -> bytes:
        return value

    def format_python_value(self, value: bytes) -> bytes:
        return value

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return Domain(), Framework()
