from typing import Tuple

from ..base import UFDLType
from ..error import expect
from .server import Domain, Framework


class Model(
    UFDLType[
        Tuple[Domain, Framework],
        bytes,
        bytes
    ]
):
    def parse_binary_value(self, value: bytes) -> bytes:
        expect(bytes, value)
        return value

    def format_python_value(self, value: bytes) -> bytes:
        expect(bytes, value)
        return value

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return Domain(), Framework()

    @property
    def is_abstract(self) -> bool:
        return False
