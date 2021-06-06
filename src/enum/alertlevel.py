from enum import Enum


class Alertlevel(Enum):
    """
    Enum that represents the pager alert levels of earthquake events.
    """
    GREEN = "green"
    """
    Green pager level
    """

    YELLO = "yello"
    """
    Yellow pager level
    """

    ORANGE = "orange"
    """
    Orange pager level
    """

    RED = "red"
    """
    Red pager level
    """
