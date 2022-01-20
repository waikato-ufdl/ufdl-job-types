class TypeDoesNotSupportJSONException(Exception):
    """
    Exception for when a type doesn't support JSON input.
    """
    def __init__(self, typename: str):
        super().__init__(
            f"Type {typename} does not support JSON values"
        )
