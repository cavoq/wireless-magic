import os
import subprocess


class NetworkInterface:

    def __init__(self, name: str):
        self.name: str = name

    def get_mac_address(self) -> str:
        mac_address_file: str = f"/sys/class/net/{self.name}/address"
        if not os.path.exists(mac_address_file):
            raise FileNotFoundError("MAC address file not found.")
        with open(mac_address_file, 'r') as file:
            mac_address: str = file.read().strip()
        return mac_address

    def get_mode(self) -> str:
        mode_file: str = f"/sys/class/net/{self.name}/type"
        if not os.path.exists(mode_file):
            raise FileNotFoundError("Mode file not found.")
        with open(mode_file, 'r') as file:
            mode: str = file.read().strip()
        if mode == "1":
            return "managed"
        if mode == "803":
            return "monitor"
        return "unknown"

    def set_mode(self, mode: str) -> bool:
        if mode not in ["managed", "monitor"]:
            raise ValueError("Mode must be either 'managed' or 'monitor'.")
        self.down()
        cmd = f"sudo iwconfig {self.name} mode {mode}"
        result = subprocess.run(cmd.split(), capture_output=True)
        print(result)
        if result.returncode != 0:
            return False
        self.up()
        return True

    def down(self) -> bool:
        cmd = f"sudo ip link set down {self.name}"
        result = subprocess.run(cmd.split(), capture_output=True)
        if result.returncode != 0:
            return False
        return True

    def up(self) -> bool:
        cmd = f"sudo ip link set up {self.name}"
        result = subprocess.run(cmd.split(), capture_output=True)
        if result.returncode != 0:
            return False
        return True

    def reset(self) -> bool:
        if not self.down():
            raise RuntimeError("Failed to set interface down.")
        if not self.up():
            raise RuntimeError("Failed to set interface up.")
        return True

    def to_string(self) -> str:
        return f"Interface: {self.name}\nMAC Address: {self.get_mac_address()}\nMode: {self.get_mode()}"
