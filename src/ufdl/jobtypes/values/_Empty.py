from ._Enumerable import Enumerable, ValueType


class Empty(Enumerable[ValueType]):
    def __init__(self):
        super().__init__()
