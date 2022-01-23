import builtins
from typing import Type, Union

from ..base import UFDLType


def is_subtype(
        type: Union[UFDLType, int, str],
        of: Union[Type[UFDLType], UFDLType, Type[int], Type[str]]
) -> bool:
    if isinstance(type, str):
        return of is str

    elif isinstance(type, int):
        return of is int

    elif isinstance(type, UFDLType):
        if of is int or of is str:
            return False

        elif isinstance(of, UFDLType):
            return type.is_subtype_of(of)

        elif isinstance(of, builtins.type) and issubclass(of, UFDLType):
            return isinstance(type, of)

        else:
            raise TypeError("of")

    else:
        raise TypeError("type")
