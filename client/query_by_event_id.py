import requests
import sys
import os

sys.path.append(os.path.abspath('..'))
from pyearthquake.earthquake_query import EarthquakeQuery


def query_by_event_id():
    # query the earthquake information by event id usc000lvb5
    event_id = "usc000lvb5"
    single_result = EarthquakeQuery.search_by_event_id(event_id=event_id)
    return single_result.get_raw_json()


def query_by_event_id_original():
    # query the earthquake information by event id usc000lvb5
    event_id = "usc000lvb5"
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&eventid={}".format(event_id)
    r = requests.get(url)
    result = r.json()
    return result


if __name__ == '__main__':
    print(query_by_event_id())
    print(query_by_event_id_original())
