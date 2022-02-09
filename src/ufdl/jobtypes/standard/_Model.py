from typing import IO, Tuple, Union

from ..base import UFDLType
from .server import Domain, Framework


class Model(
    UFDLType[
        Tuple[Domain, Framework],
        bytes
    ]
):
    def parse_binary_value(self, value: Union[bytes, IO[bytes]]) -> bytes:
        if isinstance(value, bytes):
            return value
        return value.read()

    def format_python_value(self, value: bytes) -> Union[bytes, IO[bytes]]:
        return value

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return Domain(), Framework()

    @property
    def is_abstract(self) -> bool:
        return False
