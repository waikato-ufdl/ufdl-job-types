from typing import List, Union

from ..base import UFDLType
from ..error import UnknownTypeNameException, TypeParsingException
from ..initialise import name_type_translate


def parse_type(
        type_string: str
) -> UFDLType:
    """
    Parses the string representation of a type into an actual type instance.

    :param type_string:
                The type's string representation.
    :return:
    """
    params_start = type_string.find("<")
    if params_start == -1:
        name = type_string
        args = ""
    else:
        name = type_string[:params_start]
        args = type_string[params_start:]

    type_class = name_type_translate(name)

    if type_class is None:
        raise UnknownTypeNameException(name)

    try:
        parsed_args_list = parse_args(args)
    except Exception as e:
        raise TypeParsingException(type_string) from e

    if len(parsed_args_list) == 0:
        parsed_args_list = [None]

    return type_class(*parsed_args_list)


def parse_args(args: str) -> List[Union[UFDLType, str, int]]:
    """
    Parses the string representation of a list of type arguments.

    :param args:
                The type arguments to parse.
    :return:
                The parsed types.
    """
    if args == "":
        return []

    return [parse_arg(arg) for arg in split_args(args)]


def parse_arg(arg: str) -> Union[UFDLType, str, int]:
    """
    Parses a single type-argument.

    :param arg:
                The type-argument to parse.
    :return:
                The instantiated type-argument.
    """
    # If the argument is single-quoted, it is a string-constant type argument
    if arg.startswith("'") and arg.endswith("'"):
        return arg[1:-1].replace("\\'", "'")

    #
    if arg.isidentifier():
        return parse_type(arg)

    return int(arg)


def split_args(arg_string: str) -> List[str]:
    """
    Splits a string-formatted list of type arguments into individual arguments..

    :param arg_string:
                The formatted list of type arguments.
    :return:
                A list of the individual arguments.
    """
    if not arg_string.startswith("<") or not arg_string.endswith(">"):
        raise ValueError(f"Arguments must be bracketed by <>; got {arg_string}")

    depth = 0
    quoted = False
    start = 1
    result = []
    for index, char in enumerate(arg_string):
        if quoted:
            if char == "'" and arg_string[index - 1] != "\\":
                quoted = False
        elif char == "'":
            quoted = True
        elif char == "<":
            depth += 1
        elif char == ">":
            depth -= 1
            if depth < 0:
                raise ValueError(f"Unbalanced brackets at position {index} in argument string '{arg_string}'")
        elif char == "," and depth == 1:
            result.append(arg_string[start:index].strip())
            start = index + 1

    if depth != 0:
        raise ValueError(f"Unclosed brackets in arg_string '{arg_string}'")

    return result
