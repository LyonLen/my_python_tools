import unittest

from time_lyon.lunar import get_lunar_date_str_from_date_str


class TestTimeLyon(unittest.TestCase):

    def test_demo_1(self):
        get_lunar_date_str_from_date_str("1900-01-31")

    def test_demo_2(self):
        get_lunar_date_str_from_date_str("1900-01-32")
