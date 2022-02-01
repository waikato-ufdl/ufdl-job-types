from typing import List, Tuple, Union

from ..base import UFDLType, ValueType, TRUE_CONST_SYMBOL, FALSE_CONST_SYMBOL
from ..error import TypeParsingException
from ..initialise import name_translate


def parse_type(
        type_string: str
) -> UFDLType:
    """
    Parses the string representation of a type into an actual type instance.

    :param type_string:
                The type's string representation.
    :return:
    """
    if not isinstance(type_string, str):
        raise TypeParsingException(str(type_string), "Not a string")

    # Remove whitespace
    type_string = type_string.strip()

    parsed_value_type = try_parse_value_type(type_string)
    if parsed_value_type is not None:
        return ValueType.generate_subclass(parsed_value_type)()

    args_start = type_string.find("<")
    if args_start == -1:
        name = type_string.strip()
        args = ""
    else:
        name = type_string[:args_start].strip()
        args = type_string[args_start:].strip()

    type_class = name_translate(name)

    if type_class is None:
        raise TypeParsingException(type_string, f"Unknown type-name \"{name}\"")

    if args == "":
        return type_class()

    try:
        return type_class(parse_args(args))
    except Exception as e:
        raise TypeParsingException(type_string, e) from e


def try_parse_value_type(type_string: str) -> Union[str, int, float, bool, None]:
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

    return None


def parse_args(args: str) -> Tuple[UFDLType]:
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
        raise ValueError(f"Arguments must be bracketed by <>; got \"{arg_string}\"")

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
            if depth == 0:
                break
        elif char == "," and depth == 1:
            result.append(arg_string[start:index].strip())
            start = index + 1

    if quoted:
        raise ValueError(f"Unclosed quotes in \"{arg_string}\"")
    if depth != 0:
        raise ValueError(f"Unclosed brackets in arg_string \"{arg_string}\"")
    if index != len(arg_string) - 1:
        raise ValueError(f"Extra content after closing brace in \"{arg_string}\": \"{arg_string[index + 1:]}\"")

    last_arg = arg_string[start:index].strip()

    if last_arg != "":
        result.append(last_arg)

    return result
