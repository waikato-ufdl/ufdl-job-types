from io import BytesIO
from typing import Iterable


def read_all(iterable: Iterable[bytes]) -> bytes:
    """
    Reads all bytes from the supplied iterable into a buffer.

    :param iterable:
                An iterable of bytes.
    :return:
                The collected bytes of the iterable.
    """
    buffer = BytesIO()
    for chunk in iterable:
        buffer.write(chunk)
    buffer.seek(0)
    return buffer.read()
