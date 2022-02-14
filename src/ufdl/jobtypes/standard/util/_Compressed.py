from io import BytesIO, BufferedIOBase
from typing import IO, Optional, Tuple, Union, overload
from zipfile import ZipFile

from ...base import InputType, OutputType, UFDLType, Integer
from ...error import expect


class Compressed(
    UFDLType[
        Tuple[UFDLType[Tuple[UFDLType, ...], InputType, OutputType], Integer],
        InputType,
        OutputType
    ]
):
    """
    Handles compression/decompression of values.
    """
    @overload
    def __init__(self, base_type: UFDLType[Tuple[UFDLType, ...], InputType, OutputType], compression_type: Optional[int] = None): ...
    @overload
    def __init__(self, type_args: Optional[Tuple[UFDLType[Tuple[UFDLType, ...], InputType, OutputType], Integer]] = None): ...

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], UFDLType):
                args = args[0], Integer()
        else:
            args = args[0], Integer.generate_subclass(args[1]), args[2:]

        super().__init__(*args)

    def parse_binary_value(self, value: Union[bytes, IO[bytes]]) -> InputType:
        expect((bytes, BufferedIOBase), value)
        compression = self.type_args[1].value()
        expect(int, compression)
        if isinstance(value, bytes):
            value = BytesIO(value)
        with ZipFile(value, "r", compression=compression) as zf:
            return self.type_args[0].parse_binary_value(zf.read("data"))

    def format_python_value(self, value: OutputType) -> Union[bytes, IO[bytes]]:
        compression = self.type_args[1].value()
        expect(int, compression)
        buffer = BytesIO()
        with ZipFile(buffer, "w", compression=compression) as zf:
            zf.writestr("data", self.type_args[0].format_python_value(value))
        buffer.seek(0)
        return buffer

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return UFDLType(), Integer()

    @property
    def is_abstract(self) -> bool:
        return self.type_args[0].is_abstract or type(self.type_args[1]) is Integer
