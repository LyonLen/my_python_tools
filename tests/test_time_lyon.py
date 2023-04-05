import unittest

from time_utils.lunar import get_lunar_date_str_from_date_str


class TestTimeLyon(unittest.TestCase):

    def test_demo_1(self):
        print(get_lunar_date_str_from_date_str("1900-01-31"))

    def test_demo_2(self):
        print(get_lunar_date_str_from_date_str("2023-04-05"))
