from typing import Callable, Dict, List, Optional, Union

from wai.json.raw import RawJSONObject

from ..error import NotInitialisedException
from ._not_initialised import not_initialised

# Types
ListFunction = Callable[[str, Dict[str, str]], List[RawJSONObject]]
RetrieveFunction = Callable[[str, int], RawJSONObject]
DownloadFunction = Callable[[str, int], bytes]

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
        name_to_type_map: Dict[str, type]
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
    NAME_TO_TYPE_MAP = dict(name_to_type_map)
    TYPE_TO_NAME_MAP = {}
    for name, type in name_to_type_map.items():
        if not name.isidentifier():
            raise ValueError(f"Type-name '{name}' is not a valid Python identifier")
        if type in TYPE_TO_NAME_MAP:
            raise ValueError(f"Multiple type-names detected for type {type}; mapping is not one-to-one")
        TYPE_TO_NAME_MAP[type] = name


def name_type_translate(name_or_type: Union[str, type]) -> Union[type, str, None]:
    """
    Translates a name into a type or vice-versa.

    :param name_or_type:
                The name or type to translate.
    :return:
                The name of the type or the type for the name.
                Returns None if no mapping is present.
    """
    global NAME_TO_TYPE_MAP, TYPE_TO_NAME_MAP
    mapping = NAME_TO_TYPE_MAP if isinstance(name_or_type, str) else TYPE_TO_NAME_MAP
    if mapping is None:
        raise NotInitialisedException()
    return mapping.get(name_or_type, None)


def list_function(table_name: str, filters: Dict[str, str]) -> List[RawJSONObject]:
    global LIST_FUNCTION
    return LIST_FUNCTION(table_name, filters)


def retrieve_function(table_name: str, pk: int) -> RawJSONObject:
    global RETRIEVE_FUNCTION
    return RETRIEVE_FUNCTION(table_name, pk)


def download_function(table_name: str, pk: int) -> bytes:
    global DOWNLOAD_FUNCTION
    return DOWNLOAD_FUNCTION(table_name, pk)
