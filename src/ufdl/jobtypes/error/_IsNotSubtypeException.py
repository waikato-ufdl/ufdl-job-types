class IsNotSubtypeException(Exception):
    """
    Exception for when a type is not a sub-type of a required base type.
    """
    def __init__(self, passed_typename: str, required_sub_typename: str):
        super().__init__(f"{passed_typename} is not a sub-type of {required_sub_typename}")
