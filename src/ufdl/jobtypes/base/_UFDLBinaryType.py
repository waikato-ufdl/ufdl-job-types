from abc import abstractmethod
from typing import Generic, TypeVar

from ._UFDLType import UFDLType, TypeArgsType

# The Python type that is used to represent values of a UFDLType on a worker node
PythonType = TypeVar('PythonType')


class UFDLBinaryType(
    UFDLType[TypeArgsType],
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

    @abstractmethod
    def format_python_value(self, value: PythonType) -> bytes:
        """
        Formats a Python value into binary.

        :param value:
                    The value to format.
        :return:
                    The serialised value.
        """
        raise NotImplementedError(self.format_python_value.__name__)
