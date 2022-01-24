import builtins

from ..base import UFDLType
from .._type import AnyUFDLType
from ._is_ufdl_type import is_ufdl_type


def is_subtype(
        type: AnyUFDLType,
        of: AnyUFDLType
) -> bool:
    # Make sure the given types is things that can be checked
    if not is_ufdl_type(type):
        raise TypeError("type")
    if not is_ufdl_type(of):
        raise TypeError("of")

    if isinstance(of, builtins.type):
        if issubclass(of, UFDLType):
            return isinstance(type, of) or isinstance(type, builtins.type) and issubclass(type, of)
        else:
            assert of is str or of is int
            return isinstance(type, of) or type is of

    elif isinstance(of, UFDLType):
        if isinstance(type, UFDLType):
            return type.is_subtype_of(of)
        else:
            return (
                    isinstance(type, builtins.type)
                    and issubclass(type, UFDLType)
                    and type.type_base_equivalent().is_subtype_of(of)
            )

    else:
        assert isinstance(of, (str, int))
        return builtins.type(type) is builtins.type(of) and type == of
