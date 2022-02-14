from typing import IO, Optional, Tuple, Union, overload

from ...base import UFDLType, String


class BLOB(
    UFDLType[
        Tuple[String],
        Union[bytes, IO[bytes]],
        Union[bytes, IO[bytes]]
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
            args = String.generate_subclass(args[0]),

        super().__init__(*args)

    def parse_binary_value(self, value: Union[bytes, IO[bytes]]) -> Union[bytes, IO[bytes]]:
        return value

    def format_python_value(self, value: Union[bytes, IO[bytes]]) -> Union[bytes, IO[bytes]]:
        return value

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return String(),

    @property
    def is_abstract(self) -> bool:
        return False
