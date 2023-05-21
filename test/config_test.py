import os
import unittest
import json
from src.config import Config


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        # Create a temporary test config file
        self.config_file = 'test_config.json'
        self.config_data = {
            "capture_dir": "test_captures",
            "log_dir": "test_logs"
        }
        with open(self.config_file, 'w') as f:
            json.dump(self.config_data, f)

    def tearDown(self):
        # Remove the temporary test config file
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_from_json(self):
        Config.from_json(self.config_file)
        self.assertEqual(Config.capture_dir, self.config_data['capture_dir'])
        self.assertEqual(Config.log_dir, self.config_data['log_dir'])


if __name__ == '__main__':
    unittest.main()
