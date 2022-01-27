from typing import List, Tuple

from ..error import UnknownTypeNameException, TypeParsingException
from ..initialise import name_type_translate
from ._const import TRUE_CONST_SYMBOL, FALSE_CONST_SYMBOL, SIMPLE_TYPES
from ._type import AnyUFDLType


def parse_type(
        type_string: str
) -> AnyUFDLType:
    """
    Parses the string representation of a type into an actual type instance.

    :param type_string:
                The type's string representation.
    :return:
    """
    # Remove whitespace
    type_string = type_string.strip()

    # If the argument is single-quoted, it is a string-constant type argument
    if type_string.startswith("'") and type_string.endswith("'"):
        return type_string[1:-1].replace("\\'", "'")

    # If int() can parse it, it's an int const type
    # (must be before float as float() can parse ints)
    try:
        return int(type_string)
    except ValueError:
        pass

    # If float() can parse it, it's a float const type
    try:
        return float(type_string)
    except ValueError:
        pass

    # Check if it's one of the boolean const types
    if type_string == TRUE_CONST_SYMBOL:
        return True
    elif type_string == FALSE_CONST_SYMBOL:
        return False

    args_start = type_string.find("<")
    if args_start == -1:
        name = type_string.strip()
        args = ""
    else:
        name = type_string[:args_start].strip()
        args = type_string[args_start:].strip()

    type_class = name_type_translate(name)

    if type_class is None:
        raise UnknownTypeNameException(name)

    if type_class in SIMPLE_TYPES:
        if args != "":
            raise TypeParsingException(type_string)
        return type_class

    if args == "":
        return type_class

    try:
        parsed_args = parse_args(args)
    except Exception as e:
        raise TypeParsingException(type_string) from e

    return type_class(parsed_args)


def parse_args(args: str) -> Tuple[AnyUFDLType]:
    """
    Parses the string representation of a list of type arguments.

    :param args:
                The type arguments to parse.
    :return:
                The parsed types.
    """
    if args == "":
        return tuple()

    return tuple(parse_type(arg) for arg in split_args(args))


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
