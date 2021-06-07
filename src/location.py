from abc import ABC, abstractmethod
from enum import Enum
from .geocode import _GeocodeQuery
from .key import _Key


class Location(ABC):
    """
    This is the location abstract class. After initiating the locations, clients can build a list
    of the Location object, and put it into the EarthquakeQuery constructor.
    There are 4 types of locations: Rectangle, Circle, GeoRectangle and GeoCircle. GeoRectangle and
    GeoCircle use Bing Map's "Find a Location by Query" API to search the coordinates of the location.

    Example:
    ::
        rectangle = Rectangle(36.458534, -123.399768, 38.571488, -120.927844)
        circle = Circle(36.458534, -123.399768, RadiusUnit.DEGREE, 30)
        geo_rectangle = GeoRectangle("Pittsburgh, PA")
        geo_circle = GeoCircle("San Francisco", RadiusUnit.KM, 40)
        earthquake_query = EarthquakeQuery(time=None, Location=[rectangle, circle, geo_rectangle, geo_circle])
        result = earthquake_query.search()

    To show the information about the location, use the method show.
    Example:
    ::
        rectangle1 = Rectangle(0, 0, 90, 90)
        rectangle1.show()
    The console would print:
        Rectangle with min_latitude 0, min_longitude 0, max_latitude 90, max_longitude 90.
    """

    @abstractmethod
    def get_type(self) -> str:
        """
        Abstract method for getting the type of the location
        :return: dict, the type of the location
        """
        pass

    def get_value(self) -> dict:
        """
        Abstract method for getting the value dict of the location
        :return: dict, the values of the location
        """
        pass

    @abstractmethod
    def show(self):
        """
        Abstract method for printing the information of the location
        """
        pass


class Rectangle(Location):
    def __init__(self, min_latitude=-90, min_longitude=-180, max_latitude=90, max_longitude=180):
        """
        Build a rectangle location. Requests may use any combination of these parameters.
        :param min_latitude: Limit to events with a latitude larger than the specified minimum.
                             Default value is -90.0. The range is [-90.0, 90.0] degrees.
                             NOTE: min_latitude must be less than max_latitude.
        :type min_latitude:  float
        :param min_longitude: Limit to events with a longitude larger than the specified minimum.
                             Default value is -180.0. The range is [-360.0, 360.0] degrees.
                             NOTE: rectangles may cross the date line by using a min_longitude < -180 or
                                   max_longitude > 180.
                             NOTE: min_longitude must be less than max_longitude.
        :type min_longitude:  float
        :param max_latitude: Limit to events with a latitude smaller than the specified maximum.
                             Default value is 90. The range is [-90.0, 90.0] degrees.
                             NOTE: min_latitude must be less than max_latitude.
        :type max_latitude:  float
        :param max_longitude: Limit to events with a longitude smaller than the specified maximum.
                             Default value is 180.0. The range is [-360.0, 360.0] degrees.
                             NOTE: rectangles may cross the date line by using a min_longitude < -180 or
                                   max_longitude > 180.
                             NOTE: min_longitude must be less than max_longitude.
        :type max_longitude:  float
        :raises TypeError:  If any parameter is not type float or cannot convert to float.
        :raises ValueError: If min_latitude, min_longitude, max_latitude, max_longitude is not within the range.
        :raises ValueError: If min_longitude is not less than max_longitude or
                            min_latitude is not less than max_latitude.
        :return: None
        """
        try:
            float(min_latitude)
        except:
            raise TypeError("Cannot convert min_latitude to float")

        try:
            float(min_longitude)
        except:
            raise TypeError("Cannot convert min_longitude to float")

        try:
            float(max_latitude)
        except:
            raise TypeError("Cannot convert max_latitude to float")

        try:
            float(max_longitude)
        except:
            raise TypeError("Cannot convert max_longitude to float")

        if not -90.0 <= min_latitude <= 90.0:
            raise ValueError("The range of min_latitude is [-90.0, 90.0] degrees.")

        if not -360.0 <= min_longitude <= 360.0:
            raise ValueError("The range of min_longitude is [-360.0, 360.0] degrees.")

        if not -90.0 <= max_latitude <= 90.0:
            raise ValueError("The range of max_latitude is [-90.0, 90.0] degrees.")

        if not -360.0 <= max_longitude <= 360.0:
            raise ValueError("The range of max_longitude is [-360.0, 360.0] degrees.")

        if not min_latitude < max_latitude:
            raise ValueError("min_latitude should be smaller than max_latitude")

        if not min_longitude < max_longitude:
            raise ValueError("min_longitude should be smaller than max_longitude")

        self.min_latitude = min_latitude
        self.min_longitude = min_longitude
        self.max_latitude = max_latitude
        self.max_longitude = max_longitude
        self.type = "rectangle"

    def get_min_latitude(self) -> float:
        """
        Get the min latitude.
        :return: Float, the value of min_latitude
        """
        return self.min_latitude

    def get_max_latitude(self) -> float:
        """
        Get the max latitude.
        :return: Float, the value of max_latitude
        """
        return self.max_latitude

    def get_min_longitude(self) -> float:
        """
        Get the min longitude.
        :return: Float, the value of min_longitude
        """
        return self.min_longitude

    def get_max_longitude(self) -> float:
        """
        Get the max longitude.
        :return: Float, the value of max_longitude
        """
        return self.max_longitude

    def show(self):
        """
        Print the information of the location.
        """
        print("[Rectangle] min_latitude: " + str(self.min_latitude) +
              ", min_longitude: " + str(self.min_longitude) +
              ", max_latitude: " + str(self.max_latitude) +
              ", max_longitude: " + str(self.max_longitude))

    def get_type(self) -> str:
        """
        Get the type of the Location.
        :return: The type of the location.
        """
        return self.type

    def get_value(self) -> dict:
        """
        Get the value dictionary, used in EarthquakeQuery class.
        :return: The value dict.
        """
        result = {}
        result["minlatitude"] = self.min_latitude
        result["minlongitude"] = self.min_longitude
        result["maxlatitude"] = self.max_latitude
        result["maxlongitude"] = self.max_longitude
        return result


class RadiusUnit(Enum):
    """
    The Circle object's radius unit.
    """
    KM = 0, 'kilometer'
    """
    Kilometer, default is 0
    """

    DEGREE = 1, 'a degree of latitude/longitude'
    """
    Degree, 1 degree equals 1 degree of latitude and longitude, default is 1
    """


class Circle(Location):
    def __init__(self, latitude, longitude, radius_unit=RadiusUnit.KM, radius=180):
        """
        Build a circle location. We support 2 radius units, km and degree.
        Example:
        ::
            circle1 = Circle(36.458534, -123.399768, RadiusUnit.DEGREE, 30)
            circle2 = Circle(36.458534, -123.399768, RadiusUnit.KM, 30)

        :param latitude: Specify the latitude to be used for a radius search. The range is [-90.0, 90.0] degrees.
        :type latitude: float
        :param longitude: Specify the longitude to be used for a radius search. The range is [-180.0, 180.0] degrees.
        :type longitude: float
        :param radius: Limit to events within the specified maximum number of kilometers from the geographic
                       point defined by the latitude and longitude parameters.
                       The range of radius km is [0, 20001.6] km.
                       The range of radius degree is [0, 180.0] degrees.
        :type radius: float
        :param radius_unit: The unit of radius.
        :type radius_unit: RadiusUnit
        :raises TypeError:  If latitude, longitude or radius is not type float or cannot convert to float.
        :raises ValueError: If radius_unit is not type of RadiusUnit.
        :raises ValueError: If latitude, longitude or radius is not within the range.
        """
        try:
            float(latitude)
        except:
            raise TypeError("Cannot convert latitude to float")

        try:
            float(longitude)
        except:
            raise TypeError("Cannot convert longitude to float")

        if not -90.0 <= latitude <= 90.0:
            raise ValueError("The range of latitude is [-90.0, 90.0] degrees.")

        if not -360.0 <= longitude <= 360.0:
            raise ValueError("The range of longitude is [-360.0, 360.0] degrees.")

        if not isinstance(radius_unit, RadiusUnit):
            raise TypeError("radius_unit should be instance of RadiusUnit.")

        try:
            float(radius)
        except:
            raise TypeError("Cannot convert radius to float")

        if radius_unit == RadiusUnit.KM:
            if not 0 <= radius <= 20001.6:
                raise ValueError("The range of radius is [0, 20001.6] km.")

        elif radius_unit == RadiusUnit.DEGREE:
            if not 0 <= radius <= 180:
                raise ValueError("The range of max_radius_degree is [0, 180] degrees.")
        else:
            raise ValueError("No such radius")

        self.type = "circle"
        self.latitude = latitude
        self.longitude = longitude
        self.radius_unit = radius_unit
        self.radius = radius

    def get_longitude(self) -> float:
        """
        Get the value of longitude.
        :return: Float, the value of longitude.
        """
        return self.longitude

    def get_latitude(self) -> float:
        """
        Get the value of latitude.
        :return: Float, the value of latitude.
        """
        return self.latitude

    def get_radius(self) -> float:
        """
        Get the value of radius.
        :return: Float, the value of radius.
        """
        return self.radius

    def get_radius_unit(self) -> float:
        """
        Get the unit if radius.
        :return: Float, the radius unit.
        """
        return self.radius_unit

    def show(self):
        """
        Print the information of the location.
        """
        print("[Circle] latitude: " + str(self.latitude) +
              ", longitude: " + str(self.longitude) +
              ", radius: " + str(self.radius) +
              ", unit: " + str(self.radius_unit))

    def get_type(self) -> str:
        """
        Get the type of the Location.
        :return: str, the type of the location.
        """
        return self.type

    def get_value(self) -> dict:
        """
        Get the value dictionary, used in EarthquakeQuery class.
        :return: Dict, the value dict.
        """
        result = {}
        result["latitude"] = self.latitude
        result["longitude"] = self.longitude
        if self.radius_unit == RadiusUnit.KM:
            result["maxradiuskm"] = self.radius
        else:
            result["maxradius"] = self.radius
        return result


class GeoRectangle(Rectangle):
    def __init__(self, address, latitude_distance_degree=None, longitude_distance_degree=None):
        """
        The GeoCircle class use the Bing Maps "Find a Location by Query" API to search coordinates of
        the address and initialize a rectangle shape location by the search result.
        If user provide latitude_distance_degree and longitude_distance degree, we will use the center of the location,
        and initialize a rectangle by it.
        If user do not specify the desired latitude/longitude, we will use the bounding box provided by Bing Maps.

        Example:
        ::
            geo_rectangle1 = GeoRectangle("Pittsburgh, PA")
            geo_rectangle2 = GeoRectangle("Carnegie Mellon University")
            geo_rectangle3 = GeoRectangle("5000 Forbes Ave, Pittsburgh, PA 15213, United States", 30, 30)

        To use this GeoLocation functionality, please go to
        https://docs.microsoft.com/en-us/bingmaps/getting-started/bing-maps-dev-center-help/getting-a-bing-maps-key
        and get a bing maps API key, and put it in the ./src/key.txt

        :param address: The address of the location.
        :type address: str
        :param latitude_distance_degree: The distance between min_latitude and max_latitude.
                                         Range:(0, 180.0] (Should be larger than zero.), Unit: degree.
        :type latitude_distance_degree: float
        :param longitude_distance_degree: The distance of min_longitude and max_longitude.
                                         Range: (0, 360.0] (Should be larger than zero.), unit: degree.
        :type latitude_distance_degree: float
        :raises TypeError: If the address is not string.
        :raises TypeError: If latitude_distance_degree or longitude_distance_degree is not None and is not type of
                           float or cannot convert to float.
        :raises ValueError: If latitude_distance_degree or longitude_distance_degree is out of range.
        :raises ValueError: If the API cannot find an location for the provided address.
        """

        if not isinstance(address, str):
            raise TypeError("Address is not type str.")

        if _Key.key_path is None:
            raise ValueError("To use geocode, you need to specify the key path first!")

        if latitude_distance_degree is not None and longitude_distance_degree is not None:
            try:
                float(latitude_distance_degree)
            except:
                raise TypeError("Cannot convert latitude_distance_degree to float")

            try:
                float(longitude_distance_degree)
            except:
                raise TypeError("Cannot convert longitude_distance_degree to float")

            if not 0 < latitude_distance_degree <= 180:
                raise ValueError("The range of latitude_distance_degree is [0, 180.0] degrees.")

            if not 0 < longitude_distance_degree <= 360:
                raise ValueError("The range of longitude_distance_degree is [0, 360.0] degrees.")

        geocode_query = _GeocodeQuery(_Key.key_path)
        geocode_query.set_one_line_Address(address)
        json_response = geocode_query.send_query()
        address_location = geocode_query.get_address_boxing(json_response)

        if address_location is None:
            raise ValueError(
                "We are not able to find the location of the address. Please make the address more specific.")

        if latitude_distance_degree is not None and longitude_distance_degree is not None:
            center = address_location.get_center()
            center_latitude, center_longitude = center

            min_latitude = max(-90, center_latitude - latitude_distance_degree / 2.0)
            min_longitude = max(-360, center_longitude - longitude_distance_degree / 2.0)
            max_latitude = min(90, center_latitude + latitude_distance_degree / 2.0)
            max_longitude = min(360, center_longitude + longitude_distance_degree / 2.0)
        else:
            min_latitude, min_longitude, max_latitude, max_longitude = address_location.get_bounding_box()

        super().__init__(min_latitude, min_longitude, max_latitude, max_longitude)
        self.address = address_location.get_address().get_formatted_address()

    def get_address(self) -> str:
        """
        Get the formatted address of the location. The formatted address is the official address of the location,
        for example, if the address "Pittsburgh" is searched, the formatted address would be "Pittsburgh, PA".

        :return: str, the formatted address.
        """
        return self.address

    def show(self):
        """
        Print the information of the location.
        """
        print("[GeoLocation] min_latitude: " + str(self.min_latitude) +
              ", min_longitude: " + str(self.min_longitude) +
              ", max_latitude: " + str(self.max_latitude) +
              ", max_longitude: " + str(self.max_longitude) +
              ", address: " + self.address)


class GeoCircle(Circle):
    def __init__(self, address, radius_unit=RadiusUnit.KM, radius=180):
        """
        The GeoCircle class use the Bing Maps "Find a Location by Query" API to search latitude and longitude of
        the address and initialize a circle shape location by the search result.

        Example:
        ::
            geo_circle1 = GeoCircle("Pittsburgh, PA", radius_unit=RadiusUnit.KM, radius=180)
            geo_circle2 = GeoCircle("Carnegie Mellon University", radius_unit=RadiusUnit.degree, radius=10)

        To use this GeoCircle functionality, please go to
        https://docs.microsoft.com/en-us/bingmaps/getting-started/bing-maps-dev-center-help/getting-a-bing-maps-key
        and get a bing maps API key, and put it in the ./src/key.txt

        :param address: The address of the location.
        :type address: str
        :param radius: Limit to events within the specified maximum number of kilometers from the geographic
                       point defined by the latitude and longitude parameters.
                       The range of radius km is [0, 20001.6] km.
                       The range of radius degree is [0, 180.0] degrees.
        :type radius: float
        :param radius_unit: The unit of radius.
        :type radius_unit: RadiusUnit
        :raises TypeError: If the address is not string.
        :raises ValueError: If the API cannot find an location for the provided address.
        :raises ValueError: If radius is out of range.
        """
        if not isinstance(address, str):
            raise TypeError("Address is not type str.")

        if _Key.key_path is None:
            raise ValueError("To use geocode, you need to specify the key path first!")

        geocode_query = _GeocodeQuery(_Key.key_path)
        geocode_query.set_one_line_Address(address)
        json_response = geocode_query.send_query()
        address_location = geocode_query.get_address_boxing(json_response)

        if address_location is None:
            raise ValueError(
                "We are not able to find the location of the address. Please make the address more specific.")

        center = address_location.get_center()
        super().__init__(center[0], center[1], radius_unit, radius)
        self.address = address_location.get_address().get_formatted_address()

    def get_address(self) -> str:
        """
        Get the formatted address of the location. The formatted address is the official address of the location,
        for example, if the address "Pittsburgh" is searched, the formatted address would be "Pittsburgh, PA".

        :return: str, the formatted address.
        """
        return self.address

    def show(self):
        """
        Print the information of the location.
        """
        print("[GeoCircle] latitude: " + str(self.latitude) +
              ", longitude: " + str(self.longitude) +
              ", radius: " + str(self.radius) +
              ", unit: " + str(self.radius_unit) +
              ", address: " + self.address)
