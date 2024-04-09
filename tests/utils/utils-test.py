import unittest
from utils.converter import Converter
from decimal import Decimal


class TestConverterMethods(unittest.TestCase):

    def test_hex_to_big(self):
        self.assertEqual(Converter.hex_to_big('a'), 10)
        self.assertEqual(Converter.hex_to_big('ff'), 255)
        self.assertEqual(Converter.hex_to_big('100'), 256)

    def test_wei_to_eth(self):
        self.assertEqual(Converter.wei_to_eth(1000000000000000000), 1.0)
        self.assertEqual(Converter.wei_to_eth(5000000000000000000), 5.0)

    def test_eth_to_wei(self):
        self.assertEqual(Converter.eth_to_wei(1.0), 1000000000000000000)
        self.assertEqual(Converter.eth_to_wei(5.0), 5000000000000000000)

    def test_hex_to_eth(self):
        self.assertEqual(Converter.hex_to_eth('a'), Decimal('1E-17'))
        self.assertEqual(Converter.hex_to_eth('ff'), Decimal('2.55E-16'))


    def test_format_time_to_datetime(self):
        timestamp_str = '1631800000000'  # September 16, 2021 00:00:00 UTC
        self.assertEqual(Converter.format_time_to_datetime(timestamp_str), '2021-09-16 13:46:40')


    def test_format_datetime_to_timestamp(self):
        datetime_str = '2021-09-16 00:00:00'
        self.assertEqual(Converter.format_datetime_to_timestamp(datetime_str), '1631750400')

if __name__ == '__main__':
    unittest.main()