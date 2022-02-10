import re
from typing import Tuple

V_NAME_REGEX = re.compile("^(.*) v(.*)$")


def parse_v_name(name: str) -> Tuple[str, str]:
    """
    Parses the name and version from a string of the form "{name} v{version}"
    :param name:
    :return:
    """
    match = V_NAME_REGEX.match(name)

    if match is None:
        raise Exception(f"Couldn't extract name/version from V-name '{name}'")

    return match.group(1), match.group(2)
