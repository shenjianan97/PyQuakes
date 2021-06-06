from enum import Enum


class Delete(Enum):
    """
    Enum that represents the includedeleted flag in the query parameters
    """
    INCLUDE_DELETED = True
    """
    Include deleted events in the query result
    """

    NOT_INCLUDE_DELETED = False
    """
    Not include deleted events in the query result
    """

    ONLY_DELETED = "only"
    """
    Only include deleted events in the query result
    """
