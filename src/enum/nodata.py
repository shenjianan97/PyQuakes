from enum import Enum

class Nodata(Enum):
    """
    Enum representing the values of the error code when no data is found, in the query parameters.
    """
    NO_CONTENT = 204
    """
    204 - No content
    """

    NOT_FOUND = 404
    """
    404 - Not found
    """
