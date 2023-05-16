import time
import unittest
from test.mock import MOCK_INTERFACE, CLIENT_INTERFACE
from scapy.all import sendp
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
        self.ap.start()
        self.ap.sniffer.start()
        auth_request = dot11.Dot11(addr1=MOCK_INTERFACE["mac_address"], addr2=CLIENT_INTERFACE["mac_address"],
                                   addr3=MOCK_INTERFACE["mac_address"]) / dot11.Dot11Auth(algo=0, seqnum=1, status=0)
        sendp(auth_request, iface=CLIENT_INTERFACE["name"], verbose=0)
        self.ap.sniffer.stop()
        
        
