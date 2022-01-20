class UnknownTypeNameException(Exception):
    """
    Exception for when a type is specified by name and no translation
    for that name exists.
    """
    def __init__(self, type_name: str):
        super().__init__(f"Unknown type-name '{type_name}'")
