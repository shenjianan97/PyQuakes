import os
import sys
import unittest
from datetime import datetime

import requests

sys.path.append(os.path.abspath('..'))
from src.earthquake_query import EarthquakeQuery
from src.timeframe import TimeFrame
from src.location import Rectangle, Circle, RadiusUnit, GeoRectangle
from src.enum.contributor import Contributor


class TestEarthquakeQuery(unittest.TestCase):
    def test_constructor_time_location(self):
        # Test the EarthquakeQuery constructor to see if it can successfully set time and location
        location = [Rectangle(), Circle(latitude=1, longitude=1, radius_unit=RadiusUnit.KM, radius=100)]
        time = [TimeFrame(datetime(2010, 1, 1), datetime(2011, 1, 1))]
        query = EarthquakeQuery(time=time, location=location)
        self.assertEqual(location, query.get_location())
        self.assertEqual(time, query.get_time())

    def test_constructor_kwargs_no_key(self):
        # Test the kwargs in the constructor to see if a ValueError
        # is raised if the client is trying to set a non-existing parameter
        self.assertRaises(ValueError, EarthquakeQuery, nokey="test")

    def test_constructor_kwargs_set(self):
        # Test if the client can set the other and extension parameters using kwargs in the constructor
        minmagnitude = 5
        contributor = Contributor.CONTRIBUTOR_AK
        query = EarthquakeQuery(minmagnitude=minmagnitude, contributor=contributor)
        self.assertEqual(minmagnitude, query.get_min_magnitude())
        self.assertEqual(contributor, query.get_contributor())

    def test_search_by_event_id(self):
        # Test search by event id
        event_id = "usc000lvb5"
        url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&eventid={}".format(event_id)
        response = requests.get(url)
        json1 = response.json()

        detail = EarthquakeQuery.search_by_event_id(event_id=event_id)
        self.assertEqual(json1, detail.get_raw_json())

    def test_set_methods(self):
        # Test set methods
        query = EarthquakeQuery()
        # set time
        timeframe = TimeFrame(start_time=datetime(2010, 1, 1), end_time=datetime(2011, 1, 1))
        time = [timeframe]
        query.set_time(time)
        self.assertEqual(query.get_time(), time)
        # set location
        location = [GeoRectangle("Los Angeles")]
        query.set_location(location)
        self.assertEqual(query.get_location(), location)
        # set min magnitude
        min_magnitude = 5.0
        query.set_min_magnitude(min_magnitude)
        self.assertEqual(query.get_min_magnitude(), min_magnitude)
        # set contributor
        query.set_contributor(Contributor.CONTRIBUTOR_AK)
        self.assertEqual(query.get_contributor(), Contributor.CONTRIBUTOR_AK)

    def test_get_parameters(self):
        # Test get query parameters method
        start_time = datetime(2014, 1, 1)
        end_time = datetime(2014, 1, 2)
        query = EarthquakeQuery(time=[TimeFrame(start_time, end_time)])
        parameter = {"time": [
            {"starttime": start_time.isoformat().split(".")[0], "endtime": end_time.isoformat().split(".")[0]}],
            "limit": 20000}

        self.assertEqual(parameter, query.get_query_parameters())


if __name__ == '__main__':
    unittest.main()
