from typing import Set

from ._Testable import Testable, ValueType


class Enumerable(Testable[ValueType]):
    def __init__(self, *values):
        values = set(values)
        super().__init__(lambda value: value in values)
        self._values = values

    def enumerate(self) -> Set[ValueType]:
        return set(self._values)

    def size(self) -> int:
        return len(self._values)
