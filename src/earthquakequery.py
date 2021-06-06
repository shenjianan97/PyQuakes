import requests
import urllib.parse
from enum import Enum
from typing import List

from .timeframe import TimeFrame
from .location import Location
from .enum.catalog import Catalog
from .enum.contributor import Contributor
from .enum.magnitude import Magnitude
from .enum.origin import Origin
from .enum.alertlevel import Alertlevel
from .enum.delete import Delete
from .enum.supersede import Supersede
from .result_collection import ResultCollection
from .single_result import SingleResult


class EarthquakeQuery:
    """
    A base class handles setting the parameters, sending the request to the USGS Earthquake Catalog API and getting the
    query results.

    The parameters can be set in two ways.
    1. The constructors have a time parameter to set a list of **TimeFrame**, a location parameter to set a list of
    **Location**, and all other parameters can be set using their parameter names.
    For example,
    ::
        query = EarthquakeQuery(time=[TimeFrame(datetime(2010, 1, 1), datetime(2015, 1, 1))], maxdepth=1.0)

    2. Use the corresponding set method to set the parameter value.
    For example,
    ::
        query = EarthquakeQuery()
        query.set_time([TimeFrame(datetime(2010, 1, 1), datetime(2015, 1, 1))])
        query.set_max_depth(1.0)

    Two types of result cam be returned:
        1. The client can use the constructor, different set methods to set the parameters, and then call search() to get
        the result wrapped by an instance of ResultCollection. For how to use the ResultCollection, please see refer to
        the ResultCollection class.

        2. The client can call the search_by_event_id() method to get detailed information of a single earthquake by giving
        its event id wrapped by an instance of SingleResult. For how to use the SingleResult, please see refer to
        the SingleResult class.

    Note:
        If multiple time frames and locations are set, the search() method actually does multiple search to get multiple
        results, then return the combined result in a ResultCollection instance.

    Example:
        A typical usage to search a collection of results is:
        ::
            query = EarthquakeQuery()
            query.set_time([TimeFrame(datetime(2010, 1, 1), datetime(2015, 1, 1))])
            query.set_max_depth(1.0)
            result = query.search()

        A typical usage to search a specific earthquake by its event id is:
        ::
            event_id = "usc000lvb5"
            result = EarthquakeQuery.search_by_event_id(event_id)

    For detail of all available parameter, Please refer to https://earthquake.usgs.gov/fdsnws/event/1/,
    or see the docs of different set methods for each parameter
    """

    _attribute_map = {
        "catalog": "_query_catalog",
        "contributor": "_query_contributor",
        "includeallmagnitudes": "_query_include_all_magnitudes_flag",
        "includeallorigins": "_query_include_all_origins_flag",
        "includedeleted": "_query_include_all_deleted_flag",
        "includesuperseded": "_query_include_all_superseded_flag",
        "limit": "_query_limit",
        "maxdepth": "_query_max_depth",
        "maxmagnitude": "_query_max_magnitude",
        "mindepth": "_query_min_depth",
        "minmagnitude": "_query_min_magnitude",
        "alertlevel": "_query_alert_level",
        "eventtype": "_query_event_type",
        "maxcdi": "_query_max_cdi",
        "maxgap": "_query_max_gap",
        "maxmmi": "_query_max_mmi",
        "maxsig": "_query_max_significance",
        "mincdi": "_query_min_cdi",
        "minfelt": "_query_min_feltcount",
        "mingap": "_query_min_gap",
        "minsig": "_query_min_significance",
        "nodata": "_query_nodata",
        "producttype": "_query_product_type",
        "productcode": "_query_product_code",
        "reviewstatus": "_query_review_status"
    }

    _key_to_set_method_map = {
        "catalog": "set_catalog",
        "contributor": "set_contributor",
        "includeallmagnitudes": "set_include_all_magnitudes",
        "includeallorigins": "set_include_all_origins",
        "includedeleted": "set_include_deleted",
        "includesuperseded": "set_include_superseded",
        "limit": "set_limit",
        "maxdepth": "set_max_depth",
        "maxmagnitude": "set_max_magnitude",
        "mindepth": "set_min_depth",
        "minmagnitude": "set_min_magnitude",
        "alertlevel": "set_alertlevel",
        "eventtype": "set_eventtype",
        "maxcdi": "set_max_cdi",
        "maxgap": "set_max_gap",
        "maxmmi": "set_max_mmi",
        "maxsig": "set_max_significance",
        "mincdi": "set_min_cdi",
        "minfelt": "set_min_feltcount",
        "mingap": "set_min_gap",
        "minsig": "set_min_significance",
        "nodata": "set_nodata_code",
        "producttype": ("set_product_limit", 0),
        "productcode": ("set_product_limit", 1),
        "reviewstatus": "set_reviewstatus"
    }

    _base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    def __init__(self, time: List[TimeFrame] = None, location: List[Location] = None, **kwargs):
        """
        Constructor:
            Construct a Query instance. kwargs include parameters of Other and Extension

        :param time: a list of TimeFrame instances
        :type time: List[TimeFrame]
        :param location: a list of Location instances
        :type location: List[Location]
        :param kwargs: parameters of Other and Extension
        :raises ValueError:  If key is not a parameter name
        """
        for key in kwargs.keys():
            if key not in EarthquakeQuery._key_to_set_method_map:
                raise ValueError(key + " is not a parameter")

        self._query_catalog = None
        self._query_contributor = None
        self._query_eventid = None
        self._query_include_all_magnitudes_flag = None
        self._query_include_all_origins_flag = None
        self._query_include_all_deleted_flag = None
        self._query_include_all_superseded_flag = None
        self._query_limit = 20000
        self._query_max_depth = None
        self._query_min_depth = None
        self._query_max_magnitude = None
        self._query_min_magnitude = None

        self._query_alert_level = None
        self._query_event_type = None
        self._query_max_cdi = None
        self._query_max_gap = None
        self._query_max_mmi = None
        self._query_max_significance = None
        self._query_min_cdi = None
        self._query_min_feltcount = None
        self._query_min_gap = None
        self._query_min_significance = None
        self._query_nodata = None
        self._query_product_type = None
        self._query_product_code = None
        self._query_review_status = None

        self._query_time: List[TimeFrame] = [None] if time is None else time
        self._query_location: List[Location] = [None] if location is None else location

        # set kwagrs
        method_param_map = {}
        for key, value in kwargs.items():
            # get the set method name that needs to be called
            dest = EarthquakeQuery._key_to_set_method_map[key]
            # if the method only needs one parameter
            if type(dest) == str:
                # get the reference to the method
                method_to_call = getattr(self, dest)
                # call the method
                method_to_call(value)
            else:
                # if the method needs two parameters
                # get the method name
                dest_method_name = dest[0]
                # get the position for the key value
                position = dest[1]
                # if this is the first time that one of two parameters are set
                if dest_method_name not in method_param_map:
                    # save the first parameter
                    method_param_map[dest_method_name] = {position: value}
                else:
                    # if the first parameter has been saved
                    method_param_map[dest_method_name][position] = value
                    # build two parameters in a list
                    param_list = [method_param_map[dest_method_name][0], method_param_map[dest_method_name][1]]
                    # get the method reference
                    method_to_call = getattr(self, dest_method_name)
                    # call the method
                    method_to_call(*param_list)

    @staticmethod
    def search_by_event_id(event_id: str) -> SingleResult:
        """
        Search for the detail of an earthquake by its event id.
        :param event_id: the event id of the earthquake
        :return: SingleResult
        :raises ValueError:  If the HTTP response from the USGS Earthquake API is not 200
        """
        if not isinstance(event_id, str):
            raise TypeError("event id should be a string")
        query_dict = {}
        query_dict["format"] = "geojson"
        query_dict["eventid"] = event_id
        payload_str = urllib.parse.urlencode(query_dict, safe=':')
        url = EarthquakeQuery._base_url + "?" + payload_str
        r = requests.get(url)
        if r.status_code == 200:
            return SingleResult(r.json())
        else:
            raise ValueError(r.text)

    def search(self) -> ResultCollection:
        """
        Search for a collection of results according to the parameters.

        Note:
            The default value for parameter limit is set to 20000, because the USGS earthquake API can support up to
            20000 results in a single query

        :return: ResultCollection, the collection of the results of the query
        """
        result = []
        for time_single in self._query_time:
            for location_single in self._query_location:
                result.append(self._query_single(time_single, location_single))
        result_object = ResultCollection(result)
        return result_object

    def _build_other_extension_params_dic(self) -> dict:
        result = {}

        attributes = self.__dict__
        for key in EarthquakeQuery._attribute_map:
            if EarthquakeQuery._attribute_map[key] in attributes:
                # traverse the _attribute_map to construct the parameters for other and extension
                value = attributes[EarthquakeQuery._attribute_map[key]]
                if value is None:
                    continue
                elif type(value) is Magnitude:
                    result[key] = value.value
                elif type(value) is Origin:
                    result[key] = value.value
                elif type(value) is Delete:
                    result[key] = value.value
                elif type(value) is Supersede:
                    result[key] = value.value
                elif type(value) is Alertlevel:
                    result[key] = value.value
                elif type(value) is Catalog:
                    result[key] = value.value
                elif type(value) is Contributor:
                    result[key] = value.value
                else:
                    result[key] = value
        return result

    def _query_single(self, time: TimeFrame, location: Location):
        # set the format to geojson
        query_dict = {"format": "geojson"}
        # if the time needs to be set
        if time is not None:
            # set start time
            query_dict["starttime"] = time.get_start_time_string()
            # set end time
            query_dict["endtime"] = time.get_end_time_string()
            if time.is_update_after_set():
                # if have update after, set it
                query_dict["updatedafter"] = time.get_update_after_string()
        if location is not None:
            # if the location needs to be set
            query_dict.update(location.get_value())
        # update the query dict with other and extension parameters
        query_dict.update(self._build_other_extension_params_dic())
        # build the parameters in URL
        payload_str = urllib.parse.urlencode(query_dict, safe=':')
        # append the url
        url = EarthquakeQuery._base_url + "?" + payload_str
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError(r.text)

    def get_query_parameters(self) -> dict:
        """
        Get the current parameters in a dict

        :return: Dict, a dict of query parameters that has been set in the query
        """
        query_parameters = {}
        # if the time is not just None
        if self._query_time != [None]:
            # build time list for a single request
            time_list = []
            for one in self._query_time:
                one_dict = {"starttime": one.get_start_time_string(), "endtime": one.get_end_time_string()}
                if one.is_update_after_set():
                    one_dict["updateafter"] = one.get_update_after_string()
                time_list.append(one_dict)
            query_parameters["time"] = time_list
        # if the location is not just None
        if self._query_location != [None]:
            # build location list for a single request
            query_parameters["location"] = [one.get_value() for one in self._query_location]
        attributes = self.__dict__
        for key in EarthquakeQuery._attribute_map:
            if EarthquakeQuery._attribute_map[key] in attributes:
                # get the attribute value
                value = attributes[EarthquakeQuery._attribute_map[key]]
                if value is None:
                    continue
                else:
                    query_parameters[key] = value
        return query_parameters

    def set_time(self, time: List[TimeFrame]) -> 'EarthquakeQuery':
        """
        Set the time ranges for the search query

        :param time: a list of TimeFrame instances
        :return: EarthquakeQuery, self
        """
        if time is None:
            raise TypeError("time shouldn't be none")
        self._query_time = time
        return self

    def get_time(self) -> List[TimeFrame]:
        """
        Get a list of time frames set in the query parameter

        :return: List, the list of time frames
        """
        return self._query_time

    def set_location(self, location: List[Location]) -> 'EarthquakeQuery':
        """
        Set the location of the query

        :param location: a list of Location instances

        :return: EarthquakeQuery, self
        """
        if location is None:
            raise TypeError("location shouldn't be none")
        self._query_location = location
        return self

    def get_location(self) -> List[Location]:
        """
        Get the list of location set in the query parameter

        :return: List, the list of location in the query
        """
        return self._query_location

    def set_catalog(self, catalog: Catalog) -> 'EarthquakeQuery':
        """
        Set the catalog of the earthquake query. Limit the events from a specified catalog.

        Note:
            When catalog and contributor are omitted, the most preferred
            information from any catalog or contributor for the event is returned.

        :param catalog: catalog of the earthquake query
        :type catalog: Catalog
        :return: EarthquakeQuery
        """
        if isinstance(catalog, Catalog):
            self._query_catalog = catalog
            return self
        else:
            raise TypeError("set_catalog input is not with type Catalog")

    def get_catalog(self) -> str:
        """
        Get the value of the catalog parameter

        :return: str, value of the catalog parameter
        """
        return self._query_catalog

    def set_contributor(self, contributor: Contributor) -> 'EarthquakeQuery':
        """
        Set the contributor of the earthquake query.
        Limit to events contributed by a specified contributor.

        Note:
            When catalog and contributor are omitted, the most preferred
            information from any catalog or contributor for the event is returned.

        :param contributor: contributor of the earthquake query.
        :type contributor: Contributor
        :return: EarthquakeQuery, self
        """
        if isinstance(contributor, Contributor):
            self._query_contributor = contributor
            return self
        else:
            raise TypeError("set_contributor input is not with type Contributor")

    def get_contributor(self) -> str:
        """
        Get the value of the contributor parameter

        :return: str, value of the contributor parameter
        """
        return self._query_contributor

    def set_include_all_magnitudes(self, magnitude_flag: Magnitude) -> 'EarthquakeQuery':
        """
        Set whether the query result should include all the magnitude.

        The default magnitude_flag is set to be Magnitude.NOT_INCLUDE_ALL_MAGNITUDE.

        :raise TypeError: If the magnitude_flag is not with type Enum Magnitude
               IllegalFormat: if the format of the query is not xml or quakeml.
        :param magnitude_flag: if magnitude_flag is INCLUDE_ALL_MAGNITUDE, set the query to include all the magnitude;
                               otherwise, set the query not to include all the magnitude
        :type magnitude_flag: Magnitude
        :return: EarthquakeQuery
        """
        if isinstance(magnitude_flag, Magnitude):
            self._query_include_all_magnitudes_flag = magnitude_flag
            return self
        else:
            raise TypeError("set_include_all_magnitudes input is not with type Magnitude")

    def get_include_all_magnitudes(self):
        """
        Get the status of whether the earthquake query result should include all the magnitude.

        :return: status of whether the earthquake query result should include all the magnitude
        """
        return self._query_include_all_magnitudes_flag

    def set_include_all_origins(self, origin_flag: Origin) -> 'EarthquakeQuery':
        """
        Set whether the query result should include all the origins.

        The default origin_flag is set to be Origin.NOT_INCLUDE_ALL_ORIGINS.

        :raise TypeError: If the origin_flag is not with type Enum Origin
                          IllegalFormat: if the format of the query is not xml or quakeml.
        :param origin_flag: if origin_flag is INCLUDE_ALL_ORIGINS, set the query to include all the origins;
                            otherwise, set the query not to include all the origins.
        :type origin_flag: Origin
        :return: EarthquakeQuery
        """
        if isinstance(origin_flag, Origin):
            self._query_include_all_origins_flag = origin_flag
            return self
        else:
            raise TypeError("set_include_all_origins input is not with type Origin")

    def get_include_all_origins(self):
        """
        Get the status of whether the earthquake query result should include all the origins.

        :return: status of whether the earthquake query result should include all the origins
        """
        return self._query_include_all_origins_flag

    def set_include_deleted(self, delete_flag: Delete) -> 'EarthquakeQuery':
        """
        Set whether the query result should include events that are deleted.

        The default delete_flag is set to be Delete.NOT_INCLUDE_DELETED

        :raise  TypeError: If the delete_flag is not with type Enum Delete
                IllegalFormat: if the format of the query is not geojson or csv.
        :param delete_flag: if delete_flag is INCLUDE_DELETED, the query result include the deleted events.
                            otherwise, the query result does not include the deleted events
        :type delete_flag: Delete
        :return: EarthquakeQuery
        """
        if isinstance(delete_flag, Delete):
            self._query_include_all_deleted_flag = delete_flag
            return self
        else:
            raise TypeError("set_include_deleted input is not with type Delete")

    def get_include_deleted(self) -> bool:
        """
        Get the status of whether the earthquake query result should include the deleted events.

        :return: Bool, status of whether the earthquake query result should include the deleted events.
        """
        return self._query_include_all_deleted_flag

    def set_include_superseded(self, superseded_flag: Supersede) -> 'EarthquakeQuery':
        """
        Set the query result to whether include the superseded events or products.

        The default superseded_flag is set to be NOT_INCLUDE_SUPERSEDED.

        Note: This operation will also include all deleted products.

        :raise: TypeError: If the superseded_flag is not with type Enum Supersede
                IllegalState: if the eventid is not specified.
        :param superseded_flag: if supersded_flag is INCLUDE_SUPERSEDED, the query result
                                should include the superseded events of the specified eventid;
                                otherwise, the query result should not included the superseded events.
        :type superseded_flag: Supersede
        :return: EarthquakeQuery
        """
        if isinstance(superseded_flag, Supersede):
            if self._query_eventid is not None:
                self._query_include_all_superseded_flag = superseded_flag
                return self
            else:
                raise ValueError("Query eventid is not specified.")
        else:
            raise TypeError("set_include_superseded input is not with type Supersede")

    def get_include_superseded(self) -> bool:
        """
        Get the status of whether the earthquake query result should include events being superseded.

        :return: Bool, the status of whether the earthquake query result should include events being superseded.
        """
        return self._query_include_all_superseded_flag

    def set_limit(self, limit) -> 'EarthquakeQuery':
        """
        Set the query result to a limit number.

        The limit should be an integer in the rage of 0 (inclusive) and 20000 (inclusive).
        The default limit is set to be 20000.

        :exception IllegalArgument: limit is greater than 20000 or less than 0
                                    limit is not an integer
        :param limit: limit of the earthquake query result
        :type limit: int
        :return: EarthquakeQuery
        """
        if isinstance(limit, int):
            if 0 <= limit <= 20000:
                self._query_limit = limit
            else:
                raise ValueError("set_limit input out of bound")
        else:
            raise TypeError("set_limit input should be an integer")
        return self

    def get_limit(self) -> int:
        """
        Get the limit number of a query result.

        :return: Int, limit number of a query result
        """
        return self._query_limit

    def set_max_depth(self, max_depth) -> 'EarthquakeQuery':
        """
        Set the query with limit to events with depth less than the max_depth.

        The max_depth should be in the rage of -100 (inclusive) and 1000 (inclusive).
        The default value of max_depth is set to be 1000.
        The unit of the depth is km.

        :raise ValueError: max_depth is greater than 1000 or less than -100.
        :param max_depth: max depth of an earthquake query
        :return: EarthquakeQuery
        """

        if max_depth is None:
            raise ValueError("set_max_depth input cannot be None.")
        if isinstance(max_depth, float) or isinstance(max_depth, int):
            if -100 <= max_depth <= 1000:
                self._query_max_depth = max_depth
                return self
            else:
                raise ValueError("set_max_depth input out of bounds")
        else:
            raise ValueError("set_max_depth input should be numeric.")

    def get_max_depth(self) -> float:
        """
        Get the maximum depth parameter set to the query.

        :return: float, maximum depth parameter of the query
        """
        return self._query_max_depth

    def set_max_magnitude(self, max_magnitude) -> 'EarthquakeQuery':
        """
        Set the query with limit to events with magnitude less than the max_magnitude.

        :param max_magnitude: max magnitude of an earthquake query.
        :return: EarthquakeQuery
        """
        if max_magnitude is None:
            raise ValueError("set_max_magnitude input cannot be None.")
        if isinstance(max_magnitude, float) or isinstance(max_magnitude, int):
            self._query_max_magnitude = max_magnitude
            return self
        else:
            raise ValueError("set_max_magnitude input should be numeric.")

    def get_max_magnitude(self) -> float:
        """
        Get the maximum magnitude parameter set to the query.

        :return: float, maximum magnitude parameter of the query
        """
        return self._query_max_magnitude

    def set_min_depth(self, min_depth) -> 'EarthquakeQuery':
        """
        Set the query with limit to events with depth greater than the min_depth.

        The min_depth should be in the rage of -100 (inclusive) and 1000 (inclusive).
        The default value of min_depth is set to be -100.
        The unit of the depth is km.

        :raise ValueError: min_depth is greater than 1000 or less than -100.
        :param min_depth: minimum depth of an earthquake query
        :return: EarthquakeQuery, self
        """
        if min_depth is None:
            raise ValueError("set_min_depth input cannot be None.")
        if isinstance(min_depth, float) or isinstance(min_depth, int):
            if -100 <= min_depth <= 1000:
                self._query_min_depth = min_depth
                return self
            else:
                raise ValueError("set_min_depth input out of bounds")
        else:
            raise ValueError("set_min_depth input should be numeric.")

    def get_min_depth(self) -> float:
        """
        Get the minimum depth of a query.

        :return: float, minimum depth of a query
        """
        return self._query_min_depth

    def set_min_magnitude(self, min_magnitude) -> 'EarthquakeQuery':
        """
        Set the query with limit to events with magnitude greater than the min_magnitude.

        :param min_magnitude: minimum magnitude of an earthquake query.
        :return: EarthquakeQuery
        """
        if min_magnitude is None:
            raise ValueError("set_min_magnitude input cannot be None.")
        if isinstance(min_magnitude, float) or isinstance(min_magnitude, int):
            self._query_min_magnitude = min_magnitude
            return self
        else:
            raise ValueError("set_min_magnitude input should be numeric.")

    def get_min_magnitude(self) -> float:
        """
        Get the minimum magnitude of the earthquake query.

        :return: float, minimum magnitude of the earthquake query
        """
        return self._query_min_magnitude

    def set_alertlevel(self, alert_level: Alertlevel) -> 'EarthquakeQuery':
        """
        Limit to events with a specific PAGER alert level.
        The allowed values are:
            1. alert_level=green: Limit to events with PAGER alert level "green".
            2. alert_level=yellow: Limit to events with PAGER alert level "yellow".
            3. alert_level=orange: Limit to events with PAGER alert level "orange".
            4. alert_level=red: Limit to events with PAGER alert level "red".

        :param alert_level: alert level limit for search results
        :exception IllegalArgument: If the magnitude_flag is not with type Enum Alertlevel
        :return: query itself
        """
        if alert_level is None:
            raise TypeError("IllegalArgument, alert_level input cannot be None")
        if isinstance(alert_level, Alertlevel):
            self._query_alert_level = alert_level
            return self
        raise TypeError("IllegalArgument, alert_level input should be an instance of Alertlevel enum")

    def get_alert_level(self) -> str:
        """
        Get the alert level of an earthquake query.

        :return: Str, alert level of an earthquake query
        """
        return self._query_alert_level

    def set_event_type(self, eventtype: str) -> 'EarthquakeQuery':
        """
        Limit to events of a specific type. NOTE: “earthquake” will filter non-earthquake events.

        :param eventtype: target eventtype string
        :exception: IllegalArgument: If the eventtype is not valid string
        :return: EarthquakeQuery itself
        """
        if eventtype is None:
            raise ValueError("IllegalArgument, eventtype input cannot be None")
        if isinstance(eventtype, str):
            self._query_event_type = eventtype
            return self
        raise ValueError("IllegalArgument, eventtype input should be string type")

    def get_event_type(self) -> str:
        """
        Get the event type of an earthquake query.

        :return: Str, event type of an earthquake query.
        """
        return self._query_event_type

    def set_max_cdi(self, maxcdi: float) -> 'EarthquakeQuery':
        """
        Set maximum cdi limit for query search results.

        :param maxcdi: float, [0,12], Maximum value for Maximum Community Determined Intensity reported by DYFI.
        :exception: IllegalArgument: If the maxcdi is not valid
        :return: EarthquakeQuery itself
        """
        if maxcdi is None:
            raise ValueError("IllegalArgument, maxcdi input cannot be None")
        if not (isinstance(maxcdi, float) or isinstance(maxcdi, int)):
            raise ValueError("IllegalArgument, maxcdi input should be numeric")
        if maxcdi < 0 or maxcdi > 12:
            raise ValueError("IllegalArgument, maxcdi input should be in the range of [0, 12]")
        if self._query_min_cdi is not None and maxcdi <= self._query_min_cdi:
            raise ValueError("IllegalArgument, maxcdi input should be larger than mincdi")
        self._query_max_cdi = maxcdi
        return self

    def get_max_cdi(self) -> float:
        """
        Get the maximum cdi of an earthquake query.

        :return: Flaot, maximum cdi of an earthquake query
        """
        return self._query_max_cdi

    def set_min_cdi(self, mincdi: float) -> 'EarthquakeQuery':
        """
        Set minimum cdi limit for query search results.

        :param mincdi: Decimal, Minimum value for Maximum Community Determined Intensity reported by DYFI.
        :exception IllegalArgument: If the mincdi is not valid
        :return: EarthquakeQuery itself
        """
        if mincdi is None:
            raise ValueError("IllegalArgument, mincdi input cannot be None")
        if not (isinstance(mincdi, float) or isinstance(mincdi, int)):
            raise ValueError("IllegalArgument, mincdi input should be numeric")
        if self._query_max_cdi is not None and self._query_max_cdi <= mincdi:
            raise ValueError("IllegalArgument, mincdi input should be smaller than maxcdi")
        self._query_min_cdi = mincdi
        return self

    def get_min_cdi(self) -> float:
        """
        Get the minimum cdi of an earthquake query.

        :return: Float, minimum cdi of an earthquake query.
        """
        return self._query_min_cdi

    def set_max_gap(self, maxgap: float) -> 'EarthquakeQuery':
        """
        Set the max gap parameter of the query

        :param maxgap: float, [0,360] degrees, Limit to events with no more than this azimuthal gap.
        :return: EarthquakeQuery itself
        """
        if maxgap is None:
            raise ValueError("IllegalArgument, maxgap input cannot be None")
        if not (isinstance(maxgap, float) or isinstance(maxgap, int)):
            raise ValueError("IllegalArgument, maxgap input should be numeric")
        if maxgap < 0 or maxgap > 360:
            raise ValueError("IllegalArgument, maxgap input should be in the range [0,360]")
        if self._query_min_gap is not None and maxgap <= self._query_min_gap:
            raise ValueError("IllegalArgument, maxgap input should be larger than mingap")
        self._query_max_gap = maxgap
        return self

    def get_max_gap(self) -> float:
        """
        Get the maximum gap of an earthquake query.

        :return: float, maximum gap of an earthquake query.
        """
        return self._query_max_gap

    def set_min_gap(self, mingap: float) -> 'EarthquakeQuery':
        """
        Set minimum gap limit for query search results.

        :param mingap: Float, [0,360] degrees, Limit to events with no less than this azimuthal gap.
        :exception IllegalArgument: If the mingap is not valid
        :return: EarthquakeQuery itself
        """
        if mingap is None:
            raise ValueError("IllegalArgument, mingap input cannot be None")
        if not (isinstance(mingap, float) or isinstance(mingap, int)):
            raise ValueError("IllegalArgument, mingap input should be numeric")
        if mingap < 0 or mingap > 360:
            raise ValueError("IllegalArgument, mingap input should be in the range [0,360]")
        if self._query_max_gap is not None and self._query_max_gap <= mingap:
            raise ValueError("IllegalArgument, mingap input should be smaller than maxgap")
        self._query_min_gap = mingap
        return self

    def get_min_gap(self) -> float:
        """
        Get the minimum gap of an earthquake query.

        :return: float, minimum gap of an earthquake query.
        """
        return self._query_min_gap

    def set_max_mmi(self, maxmmi: float) -> 'EarthquakeQuery':
        """
        Set mmi limit for query search results.

        :param maxmmi: Decimal [0,12], Maximum value for Maximum Modified Mercalli Intensity reported by ShakeMap.
        :exception IllegalArgument: If the maxmmi is not valid
        :return: EarthquakeQuery itself
        """
        if maxmmi is None:
            raise ValueError("IllegalArgument, maxmmi cannot be None")
        if not (isinstance(maxmmi, float) or isinstance(maxmmi, int)):
            raise ValueError("IllegalArgument, maxmmi should be numeric")
        if 0 <= maxmmi <= 12:
            self._query_max_mmi = maxmmi
            return self
        raise ValueError("IllegalArgument, maxmmi should be in the range [0,12]")

    def get_max_mmi(self) -> float:
        """
        Get the maximum mmi of an earthquake query.

        :return: Float, maximum mmi of an earthquake query.
        """
        return self._query_max_mmi

    def set_max_significance(self, maxsig: int) -> 'EarthquakeQuery':
        """
        Set maximum significance limit for query search results.

        :param maxsig: Integer, limit to events with no more than this significance.
        :exception IllegalArgument: If the maxsig is not valid
        :return: EarthquakeQuery itself
        """
        if maxsig is None:
            raise ValueError("IllegalArgument, maxsig input cannot be None")
        if not isinstance(maxsig, int):
            raise ValueError("IllegalArgument, maxsig input should be int type")
        if self._query_min_significance is not None and maxsig <= self._query_min_significance:
            raise ValueError("IllegalArgument, maxsig input should be larger than minsig")
        self._query_max_significance = maxsig
        return self

    def get_max_significance(self) -> int:
        """
        Get the maximum significance of an earthquake query.

        :return: int, maximum significance of an earthquake query.
        """
        return self._query_max_significance

    def set_min_significance(self, minsig: int) -> 'EarthquakeQuery':
        """
        Set minimum significance limit for query search results.

        :param minsig: Integer, limit to events with no less than this significance.
        :exception IllegalArgument: If the minsig is not valid
        :return: query itself
        """
        if minsig is None:
            raise ValueError("IllegalArgument, minsig input cannot be None")
        if not isinstance(minsig, int):
            raise ValueError("IllegalArgument, minsig input should be int type")
        if self._query_max_significance is not None and minsig >= self._query_max_significance:
            raise ValueError("IllegalArgument, minsig input should be smaller than maxsig")
        self._query_min_significance = minsig
        return self

    def get_min_significance(self) -> int:
        """
        Get the minimum significance of an earthquake query.

        :return: Int, minimum significance of an earthquake query.
        """
        return self._query_min_significance

    def set_min_feltcount(self, minfelt: int) -> 'EarthquakeQuery':
        """
        Set felt count limit for query search results.

        :param minfelt: Integer[1,∞], limit to events with this many DYFI responses.
        :exception IllegalArgument: If the minfelt is not valid
        :return: EarthquakeQuery itself
        """
        if minfelt is None:
            raise ValueError("IllegalArgument, minfelt input cannot be None")
        if not isinstance(minfelt, int):
            raise ValueError("IllegalArgument, minfelt input should be int type")
        if minfelt >= 1:
            self._query_min_feltcount = minfelt
            return self
        raise ValueError("IllegalArgument, minfelt input should be equal or larger than 1")

    def get_min_feltcount(self) -> int:
        """
        Get the minimum feltcount of an earthquake query.

        :return: Int, minimum feltcount of an earthquake query.
        """
        return self._query_min_feltcount

    def set_nodata_code(self, nodata: int) -> 'EarthquakeQuery':
        """
        Define the error code that will be returned when no data is found.
        :param nodata: Int, (204 or 404)
        :exception IllegalArgument: If the nodata is not valid
        :return query itself
        """
        if nodata is None:
            raise ValueError("IllegalArgument, nodata input cannot be None")
        if not isinstance(nodata, int):
            raise ValueError("IllegalArgument, nodata input should be int type")
        self._query_nodata = nodata
        return self

    def get_nodata_code(self) -> int:
        """
        Get the error code that will be returned when no data is found.

        :return: Int, error code of an earthquake query when no data is found.
        """
        return self._query_nodata

    def set_product_limit(self, producttype: str, productcode: str) -> 'EarthquakeQuery':
        """
        Set product related limit for query search results.

        :param producttype: Limit to events that have this type of product associated
        :param productcode: Limit to the event that is associated with the productcode. The event will be returned even
                            if the productcode is not the preferred code for the event.
        :exception IllegalArgument: If the producttype or productcode is not valid
        :return: EarthquakeQuery itself
        """
        if producttype is None:
            raise ValueError("IllegalArgument, producttype input cannot be None")
        if productcode is None:
            raise ValueError("IllegalArgument, productcode input cannot be None")
        if not isinstance(producttype, str):
            raise ValueError("IllegalArgument, producttype input should be string type")
        if not isinstance(productcode, str):
            raise ValueError("IllegalArgument, productcode input should be string type")
        self._query_product_type = producttype
        self._query_product_code = productcode
        return self

    def get_product_type(self) -> str:
        """
        Get the product type of an earthquake query.

        :return: Str, product type of an earthquake query.
        """
        return self._query_product_type

    def get_product_code(self) -> int:
        """
        Get the product code of an earthquake query.

        :return: int, product code of an earthquake query.
        """
        return self._query_product_code

    def set_reviewstatus(self, reviewstatus: str) -> 'EarthquakeQuery':
        """
        Limit to events with a specific review status.

        :param reviewstatus: reviewstatus=automatic limits to events with review status "automatic". reviewstatus=reviewed:
                             limits to events with review status "reviewed".
        :exception IllegalArgument: If the reviewstatus is not valid
        :return: EarthquakeQuery itself
        """
        if reviewstatus is None:
            raise ValueError("IllegalArgument, reviewstatus input cannot be None")
        if not isinstance(reviewstatus, str):
            raise ValueError("IllegalArgument, reviewstatus input should be string type")
        self._query_review_status = reviewstatus
        return self

    def get_review_status(self) -> str:
        """
        Get the review status of an earthquake query.

        :return: Str, review status of an earthquake query.
        """
        return self._query_review_status
