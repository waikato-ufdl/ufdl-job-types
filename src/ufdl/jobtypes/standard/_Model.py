from io import BufferedIOBase
from typing import IO, Tuple, Union

from ..base import UFDLType
from ..error import expect
from .server import Domain, Framework


class Model(
    UFDLType[
        Tuple[Domain, Framework],
        Union[bytes, IO[bytes]],
        Union[bytes, IO[bytes]]
    ]
):
    def parse_binary_value(self, value: Union[bytes, IO[bytes]]) -> Union[bytes, IO[bytes]]:
        expect((bytes, BufferedIOBase), value)
        return value

    def format_python_value(self, value: Union[bytes, IO[bytes]]) -> Union[bytes, IO[bytes]]:
        expect((bytes, BufferedIOBase), value)
        return value

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return Domain(), Framework()

    @property
    def is_abstract(self) -> bool:
        return False
