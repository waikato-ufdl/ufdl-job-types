import builtins
from typing import Callable, Dict, Iterator, List, Optional, Type, Union

from ufdl.json.core.filter import FilterSpec

from wai.json.raw import RawJSONObject

from ..base import UFDLType
from ..error import NotInitialisedException
from ._not_initialised import not_initialised

# Types
ListFunction = Callable[[str, FilterSpec], List[RawJSONObject]]
RetrieveFunction = Callable[[str, int], RawJSONObject]
DownloadFunction = Callable[[str, int], Union[bytes, Iterator[bytes]]]

# Name/type mappings
NAME_TO_TYPE_MAP: Optional[Dict[str, type]] = None
TYPE_TO_NAME_MAP: Optional[Dict[type, str]] = None

# Server interaction functions
LIST_FUNCTION: ListFunction = not_initialised()
RETRIEVE_FUNCTION: RetrieveFunction = not_initialised()
DOWNLOAD_FUNCTION: DownloadFunction = not_initialised()


def initialise_server(
        list_function: ListFunction,
        retrieve_function: RetrieveFunction,
        download_function: DownloadFunction,
        name_to_type_map: Dict[str, Type[UFDLType]]
):
    """
    Initialises the type-systems connection to the server.
    """
    global NAME_TO_TYPE_MAP, TYPE_TO_NAME_MAP
    global LIST_FUNCTION, RETRIEVE_FUNCTION, DOWNLOAD_FUNCTION

    LIST_FUNCTION = list_function
    RETRIEVE_FUNCTION = retrieve_function
    DOWNLOAD_FUNCTION = download_function

    # Verify and reverse the name/type mapping
    NAME_TO_TYPE_MAP = {}
    TYPE_TO_NAME_MAP = {}
    for name, type in name_to_type_map.items():
        # Names must be unique
        if name in NAME_TO_TYPE_MAP:
            raise ValueError(f"Type-name '{name}' is already in-use")

        # Names must all be valid identifiers
        if not name.isidentifier():
            raise ValueError(f"Type-name '{name}' is not a valid Python identifier")

        # Must be types of UFDLType
        if not isinstance(type, builtins.type) or not issubclass(type, UFDLType):
            raise ValueError(f"Type must be a sub-class of {UFDLType.__name__}")

        # Types must be unique
        if type in TYPE_TO_NAME_MAP:
            raise ValueError(f"Multiple type-names detected for type {type}; mapping is not one-to-one")

        NAME_TO_TYPE_MAP[name] = type
        TYPE_TO_NAME_MAP[type] = name


def name_translate(name: str) -> Optional[Type[UFDLType]]:
    """
    Translates a name into a type.

    :param name:
                The name to translate.
    :return:
                The type for the name.
                Returns None if no mapping is present.
    """
    global NAME_TO_TYPE_MAP
    if NAME_TO_TYPE_MAP is None:
        raise NotInitialisedException()
    return NAME_TO_TYPE_MAP.get(name, None)


def type_translate(type: Type[UFDLType]) -> Optional[str]:
    """
    Translates a type into a name.

    :param type:
                The type to translate.
    :return:
                The name of the type.
                Returns None if no mapping is present.
    """
    global TYPE_TO_NAME_MAP
    if TYPE_TO_NAME_MAP is None:
        raise NotInitialisedException()
    return TYPE_TO_NAME_MAP.get(type, None)


def list_function(table_name: str, filter: FilterSpec) -> List[RawJSONObject]:
    global LIST_FUNCTION
    return LIST_FUNCTION(table_name, filter)


def retrieve_function(table_name: str, pk: int) -> RawJSONObject:
    global RETRIEVE_FUNCTION
    return RETRIEVE_FUNCTION(table_name, pk)


def download_function(table_name: str, pk: int) -> Union[bytes, Iterator[bytes]]:
    global DOWNLOAD_FUNCTION
    return DOWNLOAD_FUNCTION(table_name, pk)
