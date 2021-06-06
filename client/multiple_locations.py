import requests
import sys
import os

sys.path.append(os.path.abspath('..'))
from src.location import Rectangle
from src.earthquakequery import EarthquakeQuery
from src.timeframe import TimeFrame
from datetime import datetime


def query_multiple_locations():
    # query the earthquake information of bay area and sacramento from 2020-01-01 to 2010-02-01
    bay_area = Rectangle(min_latitude=36.458534,
                         min_longitude=-123.399768,
                         max_latitude=38.571488,
                         max_longitude=-120.927844)
    sac = Rectangle(min_latitude=38.099983,
                    min_longitude=-122.525024,
                    max_latitude=39.155622,
                    max_longitude=-120.443115)
    time = TimeFrame(datetime(2010, 1, 1), datetime(2010, 2, 1))
    query = EarthquakeQuery(time=[time], location=[bay_area, sac])
    result = query.search()
    return result.get_combined_json()


def query_multiple_locations_original():
    # query the earthquake information of bay area and sacramento from 2020-01-01 to 2010-02-01
    bay_area = {
        "minlatitude": 36.458534,
        "minlongitude": -123.399768,
        "maxlatitude": 38.571488,
        "maxlongitude": -120.927844
    }

    sa = {
        "minlatitude": 38.099983,
        "minlongitude": -122.525024,
        "maxlatitude": 39.155622,
        "maxlongitude": -120.443115
    }

    time = {
        "starttime": "2010-01-01",
        "endtime": "2010-02-01"
    }
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    # build first url for bay area
    parameter1 = "format=geojson&"
    for key, value in bay_area.items():
        parameter1 += key + "=" + str(value) + "&"
    for key, value in time.items():
        parameter1 += key + "=" + str(value) + "&"
    parameter1 = parameter1[:-1]
    url_bay_area = base_url + "?" + parameter1

    # build second url for sacramento
    parameter2 = "format=geojson&"
    for key, value in sa.items():
        parameter2 += key + "=" + str(value) + "&"
    for key, value in time.items():
        parameter2 += key + "=" + str(value) + "&"
    parameter2 = parameter2[:-1]
    url_sacramento = base_url + "?" + parameter2

    query_result1 = requests.get(url_bay_area).json()
    query_result2 = requests.get(url_sacramento).json()
    query_list = [query_result1, query_result2]
    # combine results
    # features
    result_id_set = set()
    unique_features = []

    for data in query_list:
        for result in data["features"]:
            ids = result["properties"]["ids"].strip(",").split(",")
            if any(x in result_id_set for x in ids):
                continue
            else:
                result_id_set.update(ids)
                unique_features.append(result)
    # bbox
    combined_bbox = []
    for data in query_list:
        try:
            combined_bbox.append(data["bbox"])
        except:
            continue
    # metadata
    combined_metadata = {"generated": [],
                         "url": [],
                         "title": query_list[0]["metadata"]["title"],
                         "status": 200,
                         "api": query_list[0]["metadata"]["api"],
                         "count": len(unique_features)}

    for data in query_list:
        combined_metadata["generated"].append(data["metadata"]["generated"])
        combined_metadata["url"].append(data["metadata"]["url"])

    combined_json = {"type": query_list[0]["type"],
                     "metadata": combined_metadata,
                     "features": unique_features,
                     "bbox": combined_bbox}
    return combined_json


if __name__ == '__main__':
    query_multiple_locations()
    query_multiple_locations_original()
