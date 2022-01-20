from typing import Optional, Type, Union

from ..base import UFDLType, NoTypeArg
from ..initialise import name_type_translate


def format_type_args_or_params(
        *type_args: Union[Type[UFDLType], UFDLType, None, Type[str], Type[int], str, int]
) -> str:
    """
    Formats a string representation of a list of type arguments.

    :param type_args:
                The type arguments.
    :return:
                The formatted string representation.
    """
    # No angle-brackets indicates an empty argument list
    if len(type_args) == 0:
        return ""

    return f"<{', '.join(format_type_arg_or_param(type_arg) for type_arg in type_args)}>"


def format_type_class_name(
        ufdl_type_class: Type[UFDLType]
) -> str:
    """
    Formats the name of a type-class.

    :param ufdl_type_class:
                The type-class to format the name for.
    :return:
                The name of the type-class.
    """
    # Try to get the name from the map
    type_class_name: Optional[str] = name_type_translate(ufdl_type_class)

    # If it wasn't in the map, use the class name
    if type_class_name is None:
        raise ValueError(f"Unnamed type {ufdl_type_class}")

    return type_class_name


def format_type_or_type_class(
        ufdl_type: Union[Type[UFDLType], UFDLType]
) -> str:
    """
    Formats a type or type-class as a string.

    :param ufdl_type:
                The type to format. If a type is given, formats the type
                arguments. If a type-class is given, the bounds of the type parameters
                are formatted instead.
    :return:
                The type formatted as a string.
    """
    if isinstance(ufdl_type, UFDLType):
        type_name = format_type_class_name(type(ufdl_type))
        formatted_type_args = (
            format_type_args_or_params(ufdl_type.type_arg)
            if ufdl_type.type_arg is not None else
            ""
        )
    else:
        type_name = format_type_class_name(ufdl_type)
        type_arg_expected_base_type = ufdl_type.type_arg_expected_base_type()
        formatted_type_args = (
            ""
            if type_arg_expected_base_type is NoTypeArg else
            format_type_args_or_params(type_arg_expected_base_type)
        )

    return f"{type_name}{formatted_type_args}"


def format_type_arg_or_param(
        type_arg: Union[Type[UFDLType], UFDLType, None, Type[str], Type[int], str, int]
) -> str:
    """
    Formats a single type argument/parameter as a string.

    :param type_arg:
                The type argument/parameter to format.
    :return:
                The formatted string representation of the type argument/parameter.
    """
    # Type parameters which have no bound are represented by a question mark
    if type_arg is None:
        return "?"

    # Type parameters which are str or int are represented by str or int
    if type_arg is str or type_arg is int:
        return str(type_arg)

    # String-value type arguments are single-quoted, with internal single-quotes backslash-escaped
    if isinstance(type_arg, str):
        formatted_str_type_arg = type_arg.replace("'", "\\'")
        return f"'{formatted_str_type_arg}'"

    # Integer-value type arguments are just the number itself
    if isinstance(type_arg, int):
        return str(type_arg)

    # Otherwise the argument/parameter is a type/type-class, so its representation
    # is the type's/type-class' own representation
    return format_type_or_type_class(type_arg)
