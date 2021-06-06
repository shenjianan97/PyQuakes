from enum import Enum


class Magnitude(Enum):
    """
    Enum values of includeallmagnitudes flag, which indicates whether all
    magnitudes for the event should be included.
    """
    INCLUDE_ALL_MAGNITUDE = True
    """
    Include all magnitude in the query result
    """

    NOT_INCLUDE_ALL_MAGNITUDE = False
    """
    Not include all magnitude in the query result
    """
