from io import BytesIO
from typing import IO, Tuple, Union
from zipfile import ZipFile

from ...base import PythonType, UFDLType, Integer


class Compressed(
    UFDLType[
        Tuple[UFDLType[Tuple[UFDLType, ...], PythonType], Integer],
        PythonType
    ]
):
    """
    Handles compression/decompression of values.
    """
    def parse_binary_value(self, value: Union[bytes, IO[bytes]]) -> PythonType:
        if isinstance(value, bytes):
            value = BytesIO(value)
        with ZipFile(value, "r", compression=self.type_args[1].value()) as zf:
            return self.type_args[0].parse_binary_value(zf.read("data"))

    def format_python_value(self, value: PythonType) -> Union[bytes, IO[bytes]]:
        buffer = BytesIO()
        with ZipFile(buffer, "w", compression=self.type_args[1].value()) as zf:
            zf.writestr("data", self.type_args[0].format_python_value(value))
        buffer.seek(0)
        return buffer

    @classmethod
    def type_params_expected_base_types(cls) -> Tuple[UFDLType, ...]:
        return UFDLType(), Integer()

    @property
    def is_abstract(self) -> bool:
        return self.type_args[0].is_abstract or type(self.type_args[1]) is Integer
