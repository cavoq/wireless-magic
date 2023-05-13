import unittest
import subprocess
import time
from src.access_point import AccessPoint
from src.network_interface import NetworkInterface

MOCK_INTERFACE = "wlx00c0ca98ddf2"


class TestAccessPoint(unittest.TestCase):

    def setUp(self):
        self.interface = NetworkInterface(MOCK_INTERFACE)
        self.ssid = "TestAP"
        self.password = "testpassword"
        self.channel = 6
        self.ap = AccessPoint(self.interface, self.ssid,
                              self.password, self.channel)

    def tearDown(self):
        self.ap.stop()

    def test_start_stop(self):
        self.assertTrue(self.ap.start())
        time.sleep(5)
        self.assertTrue(self.ap.stop())

    def test_set_interface_mode(self, mode: str):
        cmd = f"sudo iwconfig {self.interface.name} mode {mode}"
        result = subprocess.run(cmd.split(), capture_output=True)
        return result.returncode == 0
