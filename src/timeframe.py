import datetime


class TimeFrame:
    """
    Clients can use this class to specify the time frame for a query.
    Clients should use the python built-in datetime object to initialize the time.
    Example:
    ::
        start_time = datetime.now()- timedelta(20)
        end_time = datetime.now()
        timeframe = TimeFrame(start_time, end_time)

    After initializing, build a list TimeFrame objects and put it in the EarthquakeQuery constructor.
    Example:
    ::
        start_time = datetime.now() - timedelta(20)
        end_time = datetime.now()
        timeframe1 = TimeFrame(start_time, end_time)
        timeframe2 = TimeFrame(datetime(2020, 1, 1), datetime(2021, 1, 1))
        earthquake_query = EarthquakeQuery(time=[timeframe1, timeframe2])
        result = earthquake_query.search()
    """

    def __init__(self, start_time, end_time, update_after=None):
        """
        Create a TimeFrame object with start_time, end_time and update_after.

        :param start_time: The start time of the timeframe. Limit to events on or after the specified start time.
        :param end_time: The end time of the timeframe. Limit to events on or before the specified end time.
        :param update_after: The update after time. Limit to events updated after the specified time.
        :type start_time: datetime.datetime
        :type end_time: datetime.datetime
        :type update_after: datetime.datetime
        :raises TypeError: when any parameter is not an instance of datetime.datetime
        :raises ValueError: when start_time is later than end_time
        """
        if not isinstance(start_time, datetime.datetime):
            raise TypeError("start_time should be instance of datetime.datetime")
        if start_time > end_time:
            raise ValueError("start_time should not be later than end_time")

        if not isinstance(end_time, datetime.datetime):
            raise TypeError("end_time should be instance of datetime.datetime")
        if start_time > end_time:
            raise ValueError("start_time should not be later than end_time")

        if update_after is not None and not isinstance(update_after, datetime.datetime):
            raise TypeError("update_after should be instance of datetime.datetime")

        self.end_time = end_time
        self.start_time = start_time
        self.update_after = update_after

    def set_start_time(self, start_time) -> 'TimeFrame':
        """
        Limit to events on or after the specified start time. Default value: NOW - 30 days

        :param start_time: The start time. Using the datetime object.
        :type start_time: datetime.datetime
        :raises TypeError: when start_time is not an instance of datetime.datetime
        :raises ValueError: when start_time is later than end_time
        :return: the updated timeframe object.
        """
        if not isinstance(start_time, datetime.datetime):
            raise TypeError("start_time should be instance of datetime.datetime")
        if start_time > self.end_time:
            raise ValueError("start_time should not be later than end_time")
        self.start_time = start_time
        return self

    def set_end_time(self, end_time) -> 'TimeFrame':
        """
        Limit to events on or before the specified end time. Default value: present time

        :param end_time: The end time. Using the datetime object.
        :type end_time: datetime.datetime
        :raises TypeError: when end_time is not an instance of datetime.datetime
        :raises ValueError: when start_time is later than end_time
        :return: the updated timeframe object.
        """
        if not isinstance(end_time, datetime.datetime):
            raise TypeError("end_time should be instance of datetime.datetime")
        if self.start_time > end_time:
            raise ValueError("start_time should not be later than end_time")
        self.end_time = end_time
        return self

    def set_update_after(self, update_after) -> 'TimeFrame':
        """
        Limit to events updated after the specified time. Default value: None

        :param update_after: The update after time. Using the datetime object.
        :type update_after: datetime.datetime
        :raises TypeError: when update_after is not an instance of datetime.datetime
        :return: the updated timeframe object.
        """
        if not isinstance(update_after, datetime.datetime):
            raise TypeError("update_after should be instance of datetime.datetime")
        self.update_after = update_after
        return self

    def get_start_time_string(self) -> str:
        """
        Get the start_time string in ISO8601 Date/Time format.

        :return: str, the start_time string
        """
        return self.start_time.isoformat().split(".")[0]

    def get_end_time_string(self) -> str:
        """
        Get the end_time string in ISO8601 Date/Time format.

        :return: str, he end_time string
        """
        return self.end_time.isoformat().split(".")[0]

    def get_update_after_string(self) -> str:
        """
        Get the update_after string in ISO8601 Date/Time format.
        Please use the function is_update_after_set() to make sure update_after is set before calling this method,
        otherwise it will raise NullPointerException.

        Example:
        ::
            time_frame = TimeFrame()
            if time_frame.s_update_after_set():
                time_frame.get_update_after_string()

        :return: str, the update_after string
        """
        return self.update_after.isoformat().split(".")[0]

    def is_update_after_set(self) -> bool:
        """
        Check if the update_after time is set.

        :return: bool, true if update_after is set.
        """
        return self.update_after is not None
