import os
import sys
import requests
import unittest
from src.single_result import SingleResult

sys.path.append(os.path.abspath('..'))
from src.single_result import SingleResult


class TestSingleResult(unittest.TestCase):
    def test_get_raw_json(self):
        result = SingleResult(
            requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=usc000lvb5&format=geojson").json())
        actual_result = result.get_raw_json().keys()
        expected_result = ['type', 'properties', 'geometry', 'id']
        self.assertEqual(list(actual_result), expected_result)

    def test_raw_properties(self):
        result = SingleResult(
            requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=usc000lvb5&format=geojson").json())
        actual_result = result.get_raw_properties().keys()
        expected_result = ['mag', 'place', 'time', 'updated', 'tz', 'url', 'felt', 'cdi', 'mmi', 'alert', 'status',
                           'tsunami', 'sig', 'net', 'code', 'ids', 'sources', 'types', 'nst', 'dmin', 'rms', 'gap',
                           'magType', 'type', 'title', 'products']
        self.assertEqual(list(actual_result), expected_result)

    def test_get_raw_geometry(self):
        result = SingleResult(
            requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=usc000lvb5&format=geojson").json())
        actual_result = result.get_raw_geometry()
        expected_result = "{'type': 'Point', 'coordinates': [167.249, -13.8633, 187]}"
        self.assertEqual(str(actual_result), expected_result)

    def test_get_coordinates(self):
        result = SingleResult(
            requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=usc000lvb5&format=geojson").json())
        actual_result = result.get_coordinates()
        expected_result = [167.249, -13.8633, 187]
        self.assertEqual(actual_result, expected_result)

    def test_get_magnitude(self):
        result = SingleResult(
            requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=usc000lvb5&format=geojson").json())
        actual_result = result.get_magnitude()
        expected_result = 6.5
        self.assertEqual(actual_result, expected_result)

    def test_get_title(self):
        result = SingleResult(
            requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=usc000lvb5&format=geojson").json())
        actual_result = result.get_title()
        expected_result = "M 6.5 - 32km W of Sola, Vanuatu"
        self.assertEqual(str(actual_result), expected_result)

    def test_get_location_string(self):
        result = SingleResult(
            requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=usc000lvb5&format=geojson").json())
        actual_result = result.get_location_string()
        expected_result = "32km W of Sola, Vanuatu"
        self.assertEqual(str(actual_result), expected_result)

    def test_get_epoch_time(self):
        result = SingleResult(
            requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=usc000lvb5&format=geojson").json())
        actual_result = result.get_epoch_time()
        expected_result = 1388592209000
        self.assertEqual(actual_result, expected_result)

    def test_get_webpage_url(self):
        result = SingleResult(
            requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=usc000lvb5&format=geojson").json())
        actual_result = result.get_webpage_url()
        expected_result = "https://earthquake.usgs.gov/earthquakes/eventpage/usc000lvb5"
        self.assertEqual(str(actual_result), expected_result)


if __name__ == "__main__":
    unittest.main()
