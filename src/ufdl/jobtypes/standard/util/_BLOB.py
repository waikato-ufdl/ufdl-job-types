from typing import IO, Tuple, Union

from ...base import UFDLType


class BLOB(
    UFDLType[
        tuple,
        Union[bytes, IO[bytes]],
        Union[bytes, IO[bytes]]
    ]
):
    """
    Utility type for raw binary values.
    """
    def parse_binary_value(self, value: Union[bytes, IO[bytes]]) -> Union[bytes, IO[bytes]]:
        return value

    def format_python_value(self, value: Union[bytes, IO[bytes]]) -> Union[bytes, IO[bytes]]:
        return value

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return tuple()

    @property
    def is_abstract(self) -> bool:
        return False
