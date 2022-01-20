class WrongNumberOfTypeArgsException(Exception):
    """
    Exception for when the wrong number of type arguments are passed to a generic type.
    """
    def __init__(self, typename: str, passed: int, required: int):
        super().__init__(
            f"Wrong number of type arguments passed to generic type '{typename}': "
            f"expected {required} but got {passed}"
        )
