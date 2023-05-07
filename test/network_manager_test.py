import unittest
from src.network_manager import NetworkManager


class TestNetworkManager(unittest.TestCase):
    
    def test_set_state(self):
        # Test stopping the network manager
        self.assertTrue(NetworkManager.set_state(0))
        self.assertEqual(NetworkManager.get_state(), 0)
        
        # Test starting the network manager
        self.assertTrue(NetworkManager.set_state(1))
        self.assertEqual(NetworkManager.get_state(), 1)

        # Test invalid state
        self.assertFalse(NetworkManager.set_state(2))
