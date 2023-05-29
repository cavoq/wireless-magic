import unittest
from test.mock import MOCK_INTERFACE
from src.access_point import AccessPoint
from src.network_interface import NetworkInterface
from src.config import Config


class TestAccessPoint(unittest.TestCase):

    def setUp(self):
        Config.from_json("config.json")
        self.interface = NetworkInterface(MOCK_INTERFACE["name"])
        self.ssid = "TestAP"
        self.password = "testpassword"
        self.channel = 6
        self.ap = AccessPoint(self.interface, self.ssid,
                              self.password, self.channel)

    def tearDown(self):
        self.ap.stop()

    def test_start_stop(self):
        self.assertTrue(self.ap.start())
        self.assertTrue(self.ap.stop())
