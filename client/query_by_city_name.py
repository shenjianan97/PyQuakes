import requests
import sys
import os

sys.path.append(os.path.abspath('..'))
from src.location import GeoRectangle
from src.earthquake_query import EarthquakeQuery
from src.timeframe import TimeFrame
from datetime import datetime


def query_earthquake_by_city_name():
    # query the earthquake information of Los Angeles from 2010-01-01 to 2011-01-01
    query = EarthquakeQuery(location=[GeoRectangle(address="Los Angeles")])
    query.set_time([TimeFrame(start_time=datetime(2010, 1, 1), end_time=datetime(2011, 1, 1))])
    result = query.search()
    print(result.get_combined_json())


def query_earthquake_by_city_name_original():
    # query the earthquake information of Los Angeles from 2010-01-01 to 2011-01-01
    location_parameter = {'minlatitude': 33.69681930541992, 'minlongitude': -118.68380737304688,
                          'maxlatitude': 34.35064697265625,
                          'maxlongitude': -118.13885498046875}
    time_parameter = {"starttime": "2010-01-01", "endtime": "2011-01-01"}
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    parameter = "format=geojson&"
    # append location parameter
    for key, value in location_parameter.items():
        parameter += key + "=" + str(value) + "&"
    # append time parameter
    for key, value in time_parameter.items():
        parameter += key + "=" + str(value) + "&"
    parameter = parameter[:-1]
    url = base_url + "?" + parameter
    result_json = requests.get(url).json()
    print(result_json)


if __name__ == '__main__':
    query_earthquake_by_city_name()
    query_earthquake_by_city_name_original()
