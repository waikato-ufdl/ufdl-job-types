from typing import Any, Callable, NoReturn

from ..error import NotInitialisedException


def not_initialised() -> Callable[[Any, ...], NoReturn]:
    """
    Default for all initialisation-required functions which throws an error
    stating that the function has not been initialised.
    """
    def impl(*args, **kwargs):
        raise NotInitialisedException()

    return impl
