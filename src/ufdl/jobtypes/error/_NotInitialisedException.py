class NotInitialisedException(Exception):
    """
    Exception indicating that the type system hasn't been initialised
    with the server.
    """
    def __init__(self):
        super().__init__(f"Library is not yet initialised")
