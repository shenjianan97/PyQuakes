import requests
import sys
import os

sys.path.append(os.path.abspath('..'))
from src.earthquakequery import EarthquakeQuery
from src.timeframe import TimeFrame
from datetime import datetime


def query_multiple_time():
    # query the earthquake information from 2010-01-01 to 2010-01-05, from 2010-01-10 to 2010-01-15
    # and from 2010-01-20 to 2010-01-25
    time1 = TimeFrame(start_time=datetime(2010, 1, 1), end_time=datetime(2010, 1, 5))
    time2 = TimeFrame(start_time=datetime(2010, 1, 10), end_time=datetime(2010, 1, 15))
    time3 = TimeFrame(start_time=datetime(2010, 1, 20), end_time=datetime(2010, 1, 25))
    query = EarthquakeQuery(time=[time1, time2, time3])
    combined_json = query.search().get_combined_json()
    return combined_json


def query_multiple_time_original():
    # query the earthquake information from 2010-01-01 to 2010-01-05, from 2010-01-10 to 2010-01-15
    # and from 2010-01-20 to 2010-01-25
    time1_parameter = {"starttime": "2010-01-01", "endtime": "2010-01-05"}
    time2_parameter = {"starttime": "2010-01-10", "endtime": "2010-01-15"}
    time3_parameter = {"starttime": "2010-01-20", "endtime": "2010-01-25"}
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    parameter1 = "format=geojson&"
    for key, value in time1_parameter.items():
        parameter1 += key + "=" + str(value) + "&"
    parameter1 = parameter1[:-1]
    parameter2 = "format=geojson&"
    for key, value in time2_parameter.items():
        parameter2 += key + "=" + str(value) + "&"
    parameter2 = parameter2[:-1]
    parameter3 = "format=geojson&"
    for key, value in time3_parameter.items():
        parameter3 += key + "=" + str(value) + "&"
    parameter3 = parameter3[:-1]
    print(base_url + "?" + parameter1)
    query_result1 = requests.get(base_url + "?" + parameter1).json()
    query_result2 = requests.get(base_url + "?" + parameter2).json()
    query_result3 = requests.get(base_url + "?" + parameter3).json()
    query_list = [query_result1, query_result2, query_result3]
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
    query_multiple_time()
    query_multiple_time_original()
