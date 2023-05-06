import subprocess
import time
import unittest
from src.network_interface import NetworkInterface

MOCK_INTERFACE = "wlx00c0ca98ddf2"


class TestNetworkInterface(unittest.TestCase):

    def setUp(self):
        self.interface = NetworkInterface(MOCK_INTERFACE)

    def test_reset_device(self):
        # Perform a ping to make the device busy
        ping_process = subprocess.Popen("ping google.com", shell=True)
        time.sleep(1)  # Wait for ping to start

        # Reset the device and check if it's not busy anymore
        assert self.interface.reset(MOCK_INTERFACE) == True
        assert self.interface.is_busy(MOCK_INTERFACE) == False
        
        # Stop the ping process
        ping_process.kill()

    def test_is_busy(self):
        self.interface.reset()
        subprocess.Popen("ping google.com", shell=True)
        time.sleep(1)  # Wait for ping to start
        assert self.interface.is_busy(MOCK_INTERFACE) == True
        
    def test_get_mac_address(self):
        self.assertIsInstance(self.interface.get_mac_address(), str)

    def test_get_mode(self):
        self.assertIn(self.interface.get_mode(), ["managed", "monitor"])

    def test_set_mode(self):
        self.assertTrue(self.interface.set_mode("managed"))
        self.assertTrue(self.interface.set_mode("monitor"))
        self.assertFalse(self.interface.set_mode("invalid_mode"))

    def test_scan_access_points(self):
        self.assertIsInstance(self.interface.scan_access_points(), list)

    def test_to_string(self):
        self.assertIsInstance(self.interface.to_string(), str)


if __name__ == '__main__':
    unittest.main()
