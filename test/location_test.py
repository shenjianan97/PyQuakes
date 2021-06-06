import unittest
import os
import sys
sys.path.append(os.path.abspath('..'))
from src.location import Location, Rectangle, Circle, RadiusUnit, GeoCircle, GeoRectangle


class TestRectangle(unittest.TestCase):

    def test_init_happy_path(self):
        rectangle = Rectangle(10, 10, 20, 20)
        self.assertEqual(rectangle.get_min_longitude(), 10)
        self.assertEqual(rectangle.get_min_latitude(), 10)
        self.assertEqual(rectangle.get_max_longitude(), 20)
        self.assertEqual(rectangle.get_max_latitude(), 20)
        self.assertTrue(isinstance(rectangle, Location))
        self.assertTrue(isinstance(rectangle, Rectangle))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            Rectangle("10", "10", "20", "20")

    def test_range_error(self):
        with self.assertRaises(ValueError):
            Rectangle(-100, 0, 0, 100)

    def test_min_larger_than_max(self):
        with self.assertRaises(ValueError):
            Rectangle(0, 0, -10, 10)


class TestCircle(unittest.TestCase):
    def test_init_km_happy_path(self):
        circle = Circle(10, 10, RadiusUnit.KM, 10)
        self.assertEqual(circle.get_latitude(), 10)
        self.assertEqual(circle.get_longitude(), 10)
        self.assertTrue(isinstance(circle, Location))
        self.assertTrue(isinstance(circle, Circle))
        self.assertEqual(circle.get_radius(), 10)
        self.assertEqual(circle.get_radius_unit(), RadiusUnit.KM)

    def test_init_degree_happy_path(self):
        circle = Circle(10, 10, RadiusUnit.DEGREE, 10)
        self.assertEqual(circle.get_latitude(), 10)
        self.assertEqual(circle.get_longitude(), 10)
        self.assertTrue(isinstance(circle, Location))
        self.assertTrue(isinstance(circle, Circle))
        self.assertEqual(circle.get_radius(), 10)
        self.assertEqual(circle.get_radius_unit(), RadiusUnit.DEGREE)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            Circle("10", "10")

    def test_init_range_error(self):
        with self.assertRaises(ValueError):
            Circle(200, 100)

    def test_radius_degree_range_error(self):
        with self.assertRaises(ValueError):
            Circle(0, 100, RadiusUnit.DEGREE, -1)

    def test_radius_km_range_error(self):
        with self.assertRaises(ValueError):
            Circle(0, 100, RadiusUnit.KM, 210000)


class TestGeoCircle(unittest.TestCase):
    def test_init_happy_path(self):
        geo_circle = GeoCircle("Pittsburgh", RadiusUnit.DEGREE, 30)
        self.assertTrue(isinstance(geo_circle, Location))
        self.assertTrue(isinstance(geo_circle, Circle))
        self.assertTrue(isinstance(geo_circle, GeoCircle))
        self.assertEqual(geo_circle.get_latitude(), 40.442169189453125)
        self.assertEqual(geo_circle.get_longitude(), -79.99495697021484)
        self.assertEqual(geo_circle.get_address(), "Pittsburgh, PA")
        self.assertEqual(geo_circle.get_radius_unit(), RadiusUnit.DEGREE)
        self.assertEqual(geo_circle.get_radius(), 30)

    def test_init_address_not_found(self):
        with self.assertRaises(ValueError):
            GeoCircle("afafsgaregage", RadiusUnit.DEGREE, 30)

    def test_address_type_error(self):
        with self.assertRaises(TypeError):
            GeoCircle(123, RadiusUnit.DEGREE, 30)


class TestGeoRectangle(unittest.TestCase):
    def test_init_with_lat_lon_happy_path(self):
        geo_rectangle = GeoRectangle("Pittsburgh", 30, 10)
        center_lat = 40.442169189453125
        center_lon = -79.99495697021484
        self.assertTrue(isinstance(geo_rectangle, Location))
        self.assertTrue(isinstance(geo_rectangle, Rectangle))
        self.assertTrue(isinstance(geo_rectangle, GeoRectangle))
        self.assertEqual(geo_rectangle.get_min_latitude(), center_lat - 15)
        self.assertEqual(geo_rectangle.get_min_longitude(), center_lon - 5)
        self.assertEqual(geo_rectangle.get_max_latitude(), center_lat + 15)
        self.assertEqual(geo_rectangle.get_max_longitude(), center_lon + 5)
        self.assertEqual(geo_rectangle.get_address(), "Pittsburgh, PA")

    def test_init_without_lat_lon_happy_path(self):
        geo_rectangle = GeoRectangle("Pittsburgh")
        self.assertTrue(isinstance(geo_rectangle, Location))
        self.assertTrue(isinstance(geo_rectangle, Rectangle))
        self.assertTrue(isinstance(geo_rectangle, GeoRectangle))
        self.assertEqual(geo_rectangle.get_min_latitude(), 40.36156463623047)
        self.assertEqual(geo_rectangle.get_min_longitude(), -80.09552001953125)
        self.assertEqual(geo_rectangle.get_max_latitude(), 40.50105667114258)
        self.assertEqual(geo_rectangle.get_max_longitude(), -79.86578369140625)
        self.assertEqual(geo_rectangle.get_address(), "Pittsburgh, PA")

    def test_init_address_not_found(self):
        with self.assertRaises(ValueError):
            GeoRectangle("afafsgaregage", 30, 30)

    def test_address_type_error(self):
        with self.assertRaises(TypeError):
            GeoRectangle(123, 30, 30)

    def test_latitude_longitude_type_error(self):
        with self.assertRaises(TypeError):
            GeoRectangle("Pittsburgh", "30", 10)
        with self.assertRaises(TypeError):
            GeoRectangle("Pittsburgh", 30, "10")

    def test_latitude_longitude_range_error(self):
        with self.assertRaises(ValueError):
            GeoRectangle("Pittsburgh", -10, 10)
        with self.assertRaises(ValueError):
            GeoRectangle("Pittsburgh", 30, -10)
        with self.assertRaises(ValueError):
            GeoRectangle("Pittsburgh", 200, 10)
        with self.assertRaises(ValueError):
            GeoRectangle("Pittsburgh", 30, 370)


if __name__ == '__main__':
    unittest.main()
