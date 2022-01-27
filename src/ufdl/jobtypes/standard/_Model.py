from typing import Tuple, Type, Union

from ..base import UFDLType
from .server import Domain, Framework


class Model(
    UFDLType[
        Tuple[Union[Domain, Type[Domain]], Union[Framework, Type[Framework]]],
        bytes
    ]
):
    def parse_binary_value(self, value: bytes) -> bytes:
        return value

    def format_python_value(self, value: bytes) -> bytes:
        return value

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[Type[Domain], Type[Framework]]:
        return Domain, Framework
