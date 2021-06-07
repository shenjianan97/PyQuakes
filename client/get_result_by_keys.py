import requests
import sys
import os

sys.path.append(os.path.abspath('..'))
from src.location import GeoRectangle
from src.earthquake_query import EarthquakeQuery
from src.timeframe import TimeFrame
from datetime import datetime


def get_result_by_keys():
    # get the magnitudes and titles of earthquakes happened in Los Angeles during 2010-01-01 and 2011-1-1
    query = EarthquakeQuery(time=[TimeFrame(datetime(2010, 1, 1), datetime(2011, 1, 1))])
    query.set_location([GeoRectangle("Los Angeles")])
    result = query.search()
    mag_descending = result.get_data_by_keys(keys=["mag", "title"], order_by="sig", descending=False)
    return mag_descending


def get_result_by_keys_original():
    # get the magnitudes and titles of earthquakes happened in Los Angeles during 2010-01-01 and 2011-1-1
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
    # order by sig
    result_sorted = sorted(result_json["features"], key=lambda i: i["properties"]["sig"], reverse=False)
    # get result according to keys
    mag_title = [{"mag": one["properties"]["mag"], "title": one["properties"]["title"]} for one in result_sorted]
    return mag_title


if __name__ == '__main__':
    print(get_result_by_keys())
    print(get_result_by_keys_original())
