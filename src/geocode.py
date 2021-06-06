import os
from enum import Enum

import requests
import urllib.parse
from src.address import _Address

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(ROOT_DIR, 'key.txt')


class IncludeNeighborhood(Enum):
    """
    Enum values of include_neighborhood_flag, which indicates whether to include
    the neighborhood information when acquiring geolocation of an address.

    INCLUDE_NEIGHBORHOOD is include neighborhood information when available.
    NOT_INCLUDE_NEIGHBORHOOD is not include neighborhood information.
    """
    INCLUDE_NEIGHBORHOOD = 1
    NOT_INCLUDE_NEIGHBORHOOD = 0


class IncludeAdditionalResponse(Enum):
    """
    Enum values of addition_response_flag, which indicates different response format.

    INCLUDE_QUERY_PARSE is to specify that the response will be parsed into address values,
    such as addressLine, locality, adminDistrict, and postalCode.
    INCLUDE_CISO2 is to include the two-letter ISO country code.
    INCLUDE_BOTH is to include both INCLUDE_QUERY_PARSE and INCLUDE_CISO2 functionalities.
    """
    INCLUDE_QUERY_PARSE = "queryParse"
    INCLUDE_CISO2 = "ciso2"
    INCLUDE_BOTH = "queryParse,ciso2"


class _GeoLocationInfo:
    """
    A geolocation instance, containing three important information, including the center coordinates,
    boundary box and the address of a user specified address.

    This class will be internally used by the GeocodeQuery, GeoRectangle and GeoCircle classes. Users
    do not need to worry about the initialization process.
    """

    def __init__(self, center, bbox, address):
        """
        Construct a GeoLocationInfo class.

        :param center: center coordinates of a specified location
        :param bbox: bounding box of a specified location
        :param address: formatted address of a specified location
        """
        self.center = center
        self.address = address
        self.bounding_box = bbox

    def get_address(self):
        """
        Get the formatted address of a specified location.

        :return address of the location.
        """
        return self.address

    def get_center(self):
        """
        Get the center coordinates of a specified location.

        :return center coordinates of the location.
        """
        return self.center

    def get_bounding_box(self):
        """
        Get the bounding box of a specified location.

        :return bounding box of the location.
        """
        return self.bounding_box


class _GeocodeQuery:
    """
    An instance of the GeocodeQuery. This class is aimed to get the geological information
    of the user specified address.

    This class will be internally used by the GeoRectangle and GeoCircle class. User do not need to
    worry about the query sending and result parsing processes.

    This class is not thread safe.
    """

    query_url = "http://dev.virtualearth.net/REST/v1/Locations"

    def __init__(self):
        """
        Construct a GeocodeQuery instance.
        The user specified key will be read automatically.
        """
        self.key = self.read_key()
        self.query = None
        self.include_neighborhood_flag = None
        self.max_results = None
        self.include_additional_response_flag = None

    def get_key(self):
        """
        Get the user specified key.

        :return user key.
        """
        return self.key

    def read_key(self):
        """
        Read the user specified key.

        :raise KeyError - key file doesn't exist
                          cannot read user key from key file.
        """
        if os.path.exists(KEY_PATH):
            with open(KEY_PATH, 'r') as file:
                try:
                    if os.path.getsize(KEY_PATH) != 0:
                        key = file.read().replace('\n', '')
                        return key
                    else:
                        raise KeyError("Please put user key in " + KEY_PATH)
                except:
                    raise KeyError("Cannot Read Default Key")
        else:
            raise KeyError("Cannot read key file")

    def set_include_neighborhood(self, include_neighborhood_flag: IncludeNeighborhood) -> '_GeocodeQuery':
        """
        Set whether the GeocodeQuery should include the neighborhood information if available.

        :param include_neighborhood_flag: if include_neighborhood_flag is INCLUDE_NEIGHBORHOOD, include neighborhood
                                          information if available.
                                          otherwise, not include neighborhood information.
        :type include_neighborhood_flag: IncludeNeighborhood
        :return GeocodeQuery
        """
        self.include_neighborhood_flag = include_neighborhood_flag
        return self

    def get_include_neighborhood(self):
        """
        Get the status of GeocodeQuery about whether to include the neighborhood information if available.

        :return status of whether to include the neighborhood information if available.
        """
        return self.include_neighborhood_flag

    def set_max_results(self, max_results) -> '_GeocodeQuery':
        """
        Set the max result of one time GeocodeQuery.

        max_results should be in the range of 1 (inclusive) and 20 (inclusive).

        :raise TypeError: if the input is not an integer.
               ValueError: if the input is out of bounds.
        :param max_results: user specified max result number for one time GeocodeQuery.
        :type max_results: int
        :return: GeocodeQuery
        """
        if isinstance(max_results, int):
            if 1 <= max_results <= 20:
                self.max_results = max_results
                return self
            else:
                raise ValueError("set_max_results input out of bounds")
        else:
            raise TypeError("set_max_results input is not an integer ")

    def get_max_results(self):
        """
        Get the max results of the GeocodeQuery.

        :return max results.
        """
        return self.max_results

    def set_include_additional_response(self, addition_response_flag: IncludeAdditionalResponse) -> '_GeocodeQuery':
        """
        Set whether the GeocodeQuery should include additional information in the response.

        :param addition_response_flag: if addition_response_flag is set to INCLUDE_QUERY_PARSE, include the address
                                        values in the response.
                                        if addition_response_flag is set to INCLUDE_CISO2, include the two-letter ISO
                                        country code in the response.
                                        otherwise, include both of INCLUDE_QUERY_PARSE and INCLUDE_CISO2.
        :type addition_response_flag: IncludeAdditionalResponse
        :return GeocodeQuery
        """
        self.include_additional_response_flag = addition_response_flag
        return self

    def get_include_additional_response(self):
        """
        Get the status of GeocodeQuery about whether including additional information in the response.

        :return status of whether including additional information in the response.
        """
        return self.include_additional_response_flag

    def set_one_line_Address(self, one_line_address):
        """
        Set the address of the GeocodeQuery

        :param one_line_address: query address
        """
        self.query = urllib.parse.quote(one_line_address)

    def get_one_line_Address(self):
        """
        Get the address of the GeocodeQuery.

        :return address to be queried.
        """
        return self.query

    def send_query(self):
        """
        Send the geocode query to the server and get the result in json format.

        :return response in json format.
        """
        self.query_url += "/" + self.get_one_line_Address()
        request_dict = {}
        if self.get_include_additional_response() is not None:
            request_dict["include"] = self.get_include_additional_response().value
        if self.get_include_neighborhood() is not None:
            request_dict['includeNeighborhood'] = self.get_include_neighborhood().value
        if self.get_max_results() is not None:
            request_dict['maxResults'] = self.get_max_results()
        request_dict['key'] = self.get_key()
        r = requests.get(self.query_url, request_dict)
        print(r.url)
        return r.json()

    def get_address_boxing(self, response):
        """
        Get the geolocation information of the specified

        :param response: response get from the send operation.
        :return GeoLocationInfo of a specified address
        """
        resourceSets = response['resourceSets']
        geo_location = None
        if len(resourceSets) > 0:
            resource_item = response['resourceSets'][0]
            if len(resource_item) > 0 and len(resource_item['resources']) > 0:
                resources = resource_item['resources']
                single_source_item = resources[0]
                single_source_item_center = single_source_item['point']['coordinates']
                single_source_item_bounding_box = single_source_item['bbox']
                address = single_source_item['address']
                addressLine = self._assign_key('addressLine', address)
                adminDistrict = self._assign_key('adminDistrict', address)
                adminDistrict2 = self._assign_key('adminDistrict2', address)
                countryRegion = self._assign_key('countryRegion', address)
                countryRegionIso2 = self._assign_key('countryRegionIso2', address)
                formattedAddress = self._assign_key('formattedAddress', address)
                locality = self._assign_key('locality', address)
                postalCode = self._assign_key('postalCode', address)
                single_address = _Address().set_address_line(addressLine).set_admin_district(adminDistrict) \
                    .set_admin_district2(adminDistrict2).set_country_region(countryRegion) \
                    .set_country_region_iso2(countryRegionIso2).set_formatted_address(formattedAddress) \
                    .set_locality(locality).set_postal_code(postalCode)
                geo_location = _GeoLocationInfo(single_source_item_center, single_source_item_bounding_box,
                                                single_address)
        return geo_location

    def _assign_key(self, key, address_dict):
        if key in address_dict.keys():
            return address_dict[key]
        else:
            return ""
