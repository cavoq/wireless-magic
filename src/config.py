import json

class Config:
    capture_dir: str = None
    log_dir: str = None

    @staticmethod
    def from_json(config_file: str) -> None:
        with open(config_file, 'r') as file:
            config_data = json.load(file)
            Config.capture_dir = config_data.get('capture_dir')
            Config.log_dir = config_data.get('log_dir')
