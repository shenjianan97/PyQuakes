from enum import Enum


class Origin(Enum):
    """
    Enum that represents the includeallorigins flag of earthquake query parameter.
    """
    INCLUDE_ALL_ORIGINS = True
    """
    Include all origins in the query result
    """

    NOT_INCLUDE_ALL_ORIGINS = False
    """
    Not include all origins in the query result
    """
