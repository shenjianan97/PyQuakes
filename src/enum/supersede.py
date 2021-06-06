from enum import Enum


class Supersede(Enum):
    """
    Enum values of includesuperseded flag in the query parameters
    """
    INCLUDE_SUPERSEDED = True
    """
    Include superseded events in the query result
    """

    NOT_INCLUDE_SUPERSEDED = False
    """
    Not include superseded events in the query result
    """
