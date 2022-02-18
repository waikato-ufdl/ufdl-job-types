from typing import IO, Optional, Tuple, Union, overload

from ...base import UFDLType, String
from ...error import expect


class BLOB(
    UFDLType[
        Tuple[String],
        bytes,
        bytes
    ]
):
    """
    Utility type for raw binary values.
    """
    @overload
    def __init__(self, type_hint: str): ...
    @overload
    def __init__(self, type_args: Optional[Tuple[String]] = None): ...

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            args = (String.generate_subclass(args[0])(),),

        super().__init__(*args)

    def parse_binary_value(self, value: bytes) -> bytes:
        expect(bytes, value)
        return value

    def format_python_value(self, value: bytes) -> bytes:
        expect(bytes, value)
        return value

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return String(),

    @property
    def is_abstract(self) -> bool:
        return False
