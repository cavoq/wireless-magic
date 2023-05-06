import unittest
from typing import List
from twiner import TwinerBot


class TestGetWifiInterfaces(unittest.TestCase):
    
    def setUp(self):
        self.twiner_bot = TwinerBot()
        
    def test_get_wifi_interfaces(self):
        wifi_interfaces: List[str] = self.twiner_bot.get_wifi_interfaces()
        self.assertTrue(len(wifi_interfaces) > 0)


if __name__ == '__main__':
    unittest.main()
