from ._Enumerable import Enumerable, ValueType


class Single(Enumerable[ValueType]):
    def __init__(self, value: ValueType):
        super().__init__(value)
        self._value = value

    @property
    def value(self) -> ValueType:
        return self._value
