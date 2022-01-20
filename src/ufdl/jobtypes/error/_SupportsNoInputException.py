class SupportsNoInputException(Exception):
    """
    Exception for when a type doesn't support any form of input.
    """
    def __init__(self):
        super().__init__("")