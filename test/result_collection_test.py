import os
import sys
import requests
import unittest

sys.path.append(os.path.abspath('..'))
from src.result_collection import ResultCollection


class TestResultCollection(unittest.TestCase):
	def test_remove_duplicate(self):
		result_1 = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-03&minmagnitude=5").json()
		features_1 = result_1["features"]

		result_2 = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-02&endtime=2014-01-04&minmagnitude=5").json()
		features_2 = result_2["features"]

		result_3 = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-02&endtime=2014-01-03&minmagnitude=5").json()
		features_3 = result_3["features"]

		result_4 = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-04&minmagnitude=5").json()
		features_4 = result_4["features"]

		total_json_strings = [result_1, result_2, result_3]
		result_collection = ResultCollection(total_json_strings)

		self.assertEqual(len(features_4), len(result_collection.get_combined_json()["features"]))

	def test_combine(self):
		# Testing combine metadata
		result_1 = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-03&minmagnitude=5").json()
		features_1 = result_1["features"]

		result_2 = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-02&endtime=2014-01-04&minmagnitude=5").json()
		features_2 = result_2["features"]

		result_3 = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-02&endtime=2014-01-03&minmagnitude=5").json()
		features_3 = result_3["features"]

		# result_4 = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-04&minmagnitude=5").json()
		# features_4 = result_4["features"]

		total_json_strings = [result_1, result_2, result_3]
		result_collection = ResultCollection(total_json_strings)
		expected_result = {'generated': [1620613174000, 1620613174000, 1620613175000], 'url': ['https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-03&minmagnitude=5', 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-02&endtime=2014-01-04&minmagnitude=5', 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-02&endtime=2014-01-03&minmagnitude=5'], 'title': 'USGS Earthquakes', 'status': 200, 'api': '1.10.3', 'count': 9}
		self.assertEqual(expected_result["count"], result_collection.get_metadata()["count"])

	def test_get_functions(self):
		# Testing get titles
		result_1 = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2011-01-01&endtime=2013-01-01&minmagnitude=8.0").json()
		result_collection = ResultCollection([result_1])
		expected_result = ['M 8.2 - off the west coast of northern Sumatra', 'M 8.6 - off the west coast of northern Sumatra', 'M 9.1 - 2011 Great Tohoku Earthquake, Japan']
		for i in result_collection.get_all_titles():
			if i in expected_result:
				expected_result.remove(i)
		self.assertEqual(expected_result, [])

		# Testing get magnitudes
		expected_result = [9.1, 8.6, 8.2]
		for i in result_collection.get_all_magnitudes():
			if i in expected_result:
				expected_result.remove(i)
		self.assertEqual(expected_result, [])

		# Testing get number of earthquakes
		self.assertEqual(3, result_collection.get_number_of_earthquakes())

		# Testing get bbox
		expected_result = [[92.463, 0.802, 20, 142.373, 38.297, 29]]
		self.assertEqual(str(expected_result), str(result_collection.get_boundary_box()))

		# Testing get metadata
		expected_result = ['generated', 'url', 'title', 'status', 'api', 'count']
		actual_result = list(result_collection.get_metadata().keys())
		self.assertEqual(expected_result, actual_result)

		# Testing get all 3d coordinates
		expected_result = [[92.463, 0.802, 25.1], [93.063, 2.327, 20], [142.373, 38.297, 29]]
		actual_result = list(result_collection.get_all_3d_coordinates())
		self.assertEqual(expected_result, actual_result)

		# Testing get all depths
		expected_result = [25.1, 20, 29]
		actual_result = list(result_collection.get_all_depths())
		self.assertEqual(expected_result, actual_result)

	def test_get_data_by_keys(self):
		result_1 = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2011-01-01&endtime=2013-01-01&minmagnitude=8.0").json()
		result_collection = ResultCollection([result_1])
		actual_result = result_collection.get_data_by_keys(["mag", "title", "time"])
		self.assertEqual(list(actual_result[0].keys()), ["mag", "title", "time"])

	def test_get_all_earthquake_data(self):
		result_1 = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2011-01-01&endtime=2013-01-01&minmagnitude=8.0").json()
		result_collection = ResultCollection([result_1])
		actual_result = result_collection.get_all_earthquake_data()
		self.assertEqual(3, len(actual_result))
		self.assertEqual(['type', 'properties', 'geometry', 'id'], list(actual_result[0].keys()))

	def test_get_all_simplified_data(self):
		result_1 = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2011-01-01&endtime=2013-01-01&minmagnitude=8.0").json()
		result_collection = ResultCollection([result_1])
		actual_result = result_collection.get_all_simplified_data()[0].keys()
		self.assertEqual(list(actual_result), ["title", "mag", "time", "coordinates"])

	def test_ordering(self):
		# Test order by time
		result_1 = requests.get(
			"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2011-01-01&endtime=2013-01-01&minmagnitude=8.0").json()
		result_collection = ResultCollection([result_1])
		self.assertEqual(str([8.2, 8.6, 9.1]), str(result_collection.get_all_magnitudes(order_by="time", descending=True)))
		self.assertEqual(str([9.1, 8.6, 8.2]), str(result_collection.get_all_magnitudes(order_by="time", descending=False)))

		# Test order by magnitude
		self.assertEqual(str([8.2, 8.6, 9.1]), str(result_collection.get_all_magnitudes(order_by="mag", descending=False)))
		self.assertEqual(str([9.1, 8.6, 8.2]), str(result_collection.get_all_magnitudes(order_by="mag", descending=True)))


if __name__ == '__main__':
	unittest.main()








