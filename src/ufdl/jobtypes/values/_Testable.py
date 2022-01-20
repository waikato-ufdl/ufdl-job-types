from typing import Callable

from ._ValueSet import ValueSet, ValueType


class Testable(ValueSet[ValueType]):
    def __init__(self, test: Callable[[ValueType], bool]):
        self._test = test

    def test(self, value: ValueType) -> bool:
        return self._test(value)
