import unittest
from src.network_interface import NetworkInterface

MOCK_INTERFACE = "wlx00c0ca98ddf2"


class TestNetworkInterface(unittest.TestCase):

    def setUp(self):
        self.interface = NetworkInterface(MOCK_INTERFACE)

    def test_reset_device(self):
        assert self.interface.reset() == True

    def test_is_busy(self):
        self.interface.reset()
        assert self.interface.is_busy() == False
        
    def test_get_mac_address(self):
        self.assertIsInstance(self.interface.get_mac_address(), str)

    def test_get_mode(self):
        self.assertIn(self.interface.get_mode(), ["managed", "monitor"])

    def test_set_mode(self):
        self.assertTrue(self.interface.set_mode("managed"))
        self.assertTrue(self.interface.set_mode("monitor"))
        self.assertFalse(self.interface.set_mode("invalid_mode"))

    def test_to_string(self):
        self.assertIsInstance(self.interface.to_string(), str)


if __name__ == '__main__':
    unittest.main()
