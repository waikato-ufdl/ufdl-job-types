class TypeDoesNotSupportBinaryException(Exception):
    """
    Exception for when a type doesn't support binary input.
    """
    def __init__(self, typename: str):
        super().__init__(
            f"Type {typename} does not support binary values"
        )
