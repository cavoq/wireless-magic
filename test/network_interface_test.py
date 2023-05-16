import unittest
from src.network_interface import NetworkInterface
from test.mock import MOCK_INTERFACE


class TestNetworkInterface(unittest.TestCase):

    def setUp(self):
        self.interface = NetworkInterface(MOCK_INTERFACE["name"])

    def test_get_mac_address(self):
        self.assertIsInstance(self.interface.get_mac_address(), str)

    def test_get_mode(self):
        self.assertIn(self.interface.get_mode(), ["managed", "monitor"])

    def test_reset_device(self):
        assert self.interface.reset() == True
    
    def test_down_device(self):
        assert self.interface.down() == True
        
    def test_up_device(self):
        assert self.interface.up() == True
        
    def test_get_mac_address(self):
        self.assertIsInstance(self.interface.get_mac_address(), str)

    def test_get_mode(self):
        self.assertIn(self.interface.get_mode(), ["managed", "monitor"])

    def test_set_mode(self):
        self.assertRaises(ValueError, self.interface.set_mode, "foo")
        self.assertTrue(self.interface.set_mode("managed"))
        self.assertTrue(self.interface.set_mode("monitor"))

    def test_to_string(self):
        self.assertIsInstance(self.interface.to_string(), str)


if __name__ == '__main__':
    unittest.main()
