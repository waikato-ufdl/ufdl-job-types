from abc import abstractmethod
from typing import Generic

from ._PythonType import PythonType
from ._UFDLType import UFDLType, TypeArgType


class UFDLBinaryType(
    UFDLType[TypeArgType],
    Generic[PythonType],
    abstract=True
):
    """
    TODO
    """
    @abstractmethod
    def parse_binary_value(self, value: bytes) -> PythonType:
        """
        Parses a raw value supplied as binary into the Python-type.

        :param value:
                    The value to parse, as binary.
        :return:
                    The value parsed into Python.
        """
        raise NotImplementedError(self.parse_binary_value.__name__)
