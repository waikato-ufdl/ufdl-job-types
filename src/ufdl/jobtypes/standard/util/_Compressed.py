from io import BytesIO, BufferedIOBase
from typing import IO, Tuple, Union
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
