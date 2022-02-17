"""
Controls initialisation of the library for communication with the server. This is
designed so when the library is used on the server, it can provide implementations
that make native calls to the database, but when it is used on a worker node, it can
provide implementations that make REST API calls to the server instance.
"""
from ._initialisation import (
    initialise_server,
    name_translate,
    type_translate,
    list_function,
    retrieve_function,
    download_function,
    ListFunction,
    RetrieveFunction,
    DownloadFunction
)
from ._not_initialised import not_initialised
