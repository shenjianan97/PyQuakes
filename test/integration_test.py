import os
import sys
import unittest
import urllib.parse
from datetime import datetime

import requests

sys.path.append(os.path.abspath('..'))
from src.earthquakequery import EarthquakeQuery, Contributor
from src.timeframe import TimeFrame
from src.location import Rectangle, GeoRectangle
from src.result_collection import ResultCollection


class IntegrationTest(unittest.TestCase):
    def test_time_location(self):
        # Test to see if the API can get the correct result according to time and location
        bay_area = Rectangle(min_latitude=36.458534,
                             min_longitude=-123.399768,
                             max_latitude=38.571488,
                             max_longitude=-120.927844)
        time = [TimeFrame(datetime(2010, 1, 1), datetime(2010, 3, 1))]
        query = EarthquakeQuery(time=time, location=[bay_area])
        result_collection = query.search()

        base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        parameters = {
            "format": "geojson",
            "starttime": "2010-01-01",
            "endtime": "2010-03-01",
            "limit": 20000,
            "minlatitude": 36.458534,
            "minlongitude": -123.399768,
            "maxlatitude": 38.571488,
            "maxlongitude": -120.927844
        }
        payload_str = urllib.parse.urlencode(parameters, safe=':')
        result = requests.get(base_url + "?" + payload_str)
        self.assertEqual(result.json()["metadata"]["count"], result_collection.get_number_of_earthquakes())

    def test_search_by_event_id(self):
        # Test search by event id, using the API to get specific content. See if the content is correct.
        event_id = "usc000lvb5"
        single_result = EarthquakeQuery.search_by_event_id(event_id=event_id)
        actual_result = single_result.get_raw_geometry()
        expected_result = "{'type': 'Point', 'coordinates': [167.249, -13.8633, 187]}"
        expected_magnitude = 6.5
        self.assertEqual(str(actual_result), expected_result)
        self.assertEqual(single_result.get_magnitude(), expected_magnitude)
        self.assertEqual(single_result.get_location_string(), "32km W of Sola, Vanuatu")

    def test_empty_result(self):
        # Test if there is no earthquake information if the magnitude threshold is too high,
        # and no exception will happen
        query = EarthquakeQuery(time=[TimeFrame(datetime(2010, 1, 1), datetime(2010, 1, 2))])
        query.set_min_magnitude(9)
        result = query.search()
        self.assertEqual(result.get_number_of_earthquakes(), 0)

    def test_search_get_data_by_keys(self):
        # Test using the set methods in EarthquakeQuery and get data by key
        # in the ResultCollection to see if the data is correct
        result_1 = requests.get(
            "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2011-01-01&endtime=2013-01-01"
            "&minmagnitude=8.0&contributor=ak").json()
        result_collection = ResultCollection([result_1])
        title_result = result_collection.get_data_by_keys(["title"])

        query = EarthquakeQuery(time=[TimeFrame(datetime(2011, 1, 1), datetime(2013, 1, 1))], minmagnitude=8.0,
                                contributor=Contributor.CONTRIBUTOR_AK)
        result_collection2 = query.search()
        title_result2 = result_collection2.get_data_by_keys(["title"])
        self.assertEqual(title_result, title_result2)

    def test_values_ordering(self):
        # Test the query function and the value ordering function in ResultCollection
        query = EarthquakeQuery(time=[TimeFrame(datetime(2011, 1, 1), datetime(2013, 1, 1))], minmagnitude=8.0)
        result_collection = query.search()
        # test titles
        expected_titles = ['M 8.2 - off the west coast of northern Sumatra',
                           'M 8.6 - off the west coast of northern Sumatra',
                           'M 9.1 - 2011 Great Tohoku Earthquake, Japan']
        self.assertEqual(expected_titles, result_collection.get_all_titles())

        # test magnitudes values
        expected_magnitudes = [9.1, 8.6, 8.2]
        self.assertEqual(expected_magnitudes, result_collection.get_all_magnitudes())

        # test metadata values
        expected_metadata = ['generated', 'url', 'title', 'status', 'api', 'count']
        actual_result = list(result_collection.get_metadata().keys())
        self.assertEqual(expected_metadata, actual_result)

        # test ordering
        self.assertEqual(str([8.2, 8.6, 9.1]),
                         str(result_collection.get_all_magnitudes(order_by="time", descending=True)))

    def test_geolocation(self):
        # Test if there is no earthquake information for Pittsburgh (Pittsburgh is not in the earthquake zone)
        location = [GeoRectangle("Pittsburgh, PA")]
        query = EarthquakeQuery(time=[TimeFrame(datetime(2010, 1, 1), datetime(2010, 4, 1))])
        query.set_location(location=location)
        result_collection = query.search()
        # no earthquakes in Pittsburgh
        self.assertEqual(result_collection.get_number_of_earthquakes(), 0)

    def test_multiple_time_location(self):
        # Test if the API can handle multiple-time-location search
        bay_area = Rectangle(min_latitude=36.458534,
                             min_longitude=-123.399768,
                             max_latitude=38.571488,
                             max_longitude=-120.927844)
        sac = Rectangle(min_latitude=38.099983,
                        min_longitude=-122.525024,
                        max_latitude=39.155622,
                        max_longitude=-120.443115)
        time1 = TimeFrame(datetime(2010, 1, 1), datetime(2010, 1, 2))
        time2 = TimeFrame(datetime(2010, 1, 2), datetime(2010, 1, 3))
        time3 = TimeFrame(datetime(2010, 1, 3), datetime(2010, 1, 4))
        time_multiple = [time1, time2, time3]
        query_multiple = EarthquakeQuery(time=time_multiple, location=[bay_area, sac])
        multiple_result = query_multiple.search()
        query_combine = EarthquakeQuery(time=[TimeFrame(datetime(2010, 1, 1), datetime(2010, 1, 4))], location=[bay_area, sac])
        combine_result = query_combine.search()
        self.assertEqual(multiple_result.get_number_of_earthquakes(), combine_result.get_number_of_earthquakes())


if __name__ == '__main__':
    unittest.main()
