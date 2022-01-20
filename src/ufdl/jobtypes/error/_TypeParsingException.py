class TypeParsingException(Exception):
    """
    Exception for when there is an error parsing a type-string.
    """
    def __init__(self, type_string: str):
        super().__init__(f"Error parsing type-string '{type_string}'")
