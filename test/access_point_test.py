import unittest
from test.mock import MOCK_INTERFACE
from scapy.layers import dot11
from src.access_point import AccessPoint
from src.network_interface import NetworkInterface


class TestAccessPoint(unittest.TestCase):

    def setUp(self):
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

    def test_sniff_connection_request(self):
        connection_request = dot11.RadioTap()/dot11.Dot11(type=0, subtype=4, addr1="ff:ff:ff:ff:ff:ff",
                                                          addr2="00:c0:ca:98:dd:f2", addr3="00:c0:ca:98:dd:f2")/dot11.Dot11ProbeReq()
