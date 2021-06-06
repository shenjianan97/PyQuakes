from datetime import datetime


class SingleResult:
    """
    This class represents the result data of a single earthquake event. In the USGS REST API,
    searching for a range (time/location) gives a collection of events, which is named as
    **FeatureCollection** in GeoJSON standard. Searching with a particular event ID gives us a
    single event, which is named **Feature** in GeoJSON standard.

    This class accepts all the json data that the query generated, processes the data, and provides
    users all the necessary APIs for getting ordered, sorted and simplified results. The APIs are specially
    designed to include all functionality of the USGS API.

    Example:
    ::
        event_id = "usc000lvb5"
        single_result = EarthquakeQuery.search_by_event_id(event_id=event_id)
        single_result.get_raw_json()


    """
    def __init__(self, result_json):
        """
		Constructor:
			Saves the query result json string as class attribute

		:param result_json: str, query result json string
		"""

        self.json_raw = result_json

    def get_raw_json(self) -> str:
        """
        Get a raw json file which describes a single earthquake

        :return: str, raw json string
        """
        return self.json_raw

    def get_raw_properties(self) -> dict:
        """
        Get properties of a individual earthquake, i.e. mag, title, etc.

        :return: dict, a dictionary contains all properties attributes of an earthquake
        """
        return self.json_raw["properties"]

    def get_raw_geometry(self) -> dict:
        """
        Get geometry of an individual earthquake, i.e. type and coordinates

        :return: dict, a dictionary, contains all geometry info of an earthquake
        """
        return self.json_raw["geometry"]

    def get_coordinates(self) -> list:
        """
        Get coordinates of where the individual earthquake source centered

        :return: list, a list of the coordinates, which has latitude, longitude, and elevation info
        """
        return self.json_raw["geometry"]["coordinates"]

    def get_magnitude(self) -> float:
        """
        Get the magnitude of the earthquake, measuring of the size of the earthquake source

        :return: float, the magnitude of the earthquake
        """
        return self.json_raw["properties"]["mag"]

    def get_title(self) -> str:
        """
        Get the title of the earthquake, containing the basic info describing the earthquake,
        i.e. "M 6.5 - 32km W of Sola, Vanuatu"

        :return: str, the title of the earthquake
        """
        return self.json_raw["properties"]["title"]

    def get_location_string(self) -> str:
        """
        Get the location of the earthquake, describing the direction from the nearby city.
        For example: '32km W of Sola, Vanuatu'

        :return: str, the location of the earthquake
        """
        return self.json_raw["properties"]["place"]

    def get_epoch_time(self) -> int:
        """
        Get the epoch time of the earthquake happened

        :return: int, the epoch time
        """
        return self.json_raw["properties"]["time"]

    def get_datetime(self) -> datetime:
        """
        Convert the epoch time to datetime in Python

        :return: datetime, the converted datetime object from epoch time
        """
        return datetime.fromtimestamp(self.json_raw["properties"]["time"] / 1000.0)

    def get_webpage_url(self) -> str:
        """
        Get the web page URL of this particular earthquake event

        :return: str, the web page URL of this event
        """
        return self.json_raw["properties"]["url"]
