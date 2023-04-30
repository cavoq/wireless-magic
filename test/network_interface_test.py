import unittest
from typing import List
from src.network_interface import get_wifi_interfaces


class TestGetWifiInterfaces(unittest.TestCase):
    def test_get_wifi_interfaces(self):
        wifi_interfaces: List[str] = get_wifi_interfaces()
        self.assertTrue(len(wifi_interfaces) > 0)


if __name__ == '__main__':
    unittest.main()
