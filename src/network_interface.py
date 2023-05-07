import os
import subprocess
import time
from typing import List


class NetworkInterface:

    def __init__(self, name: str):
        self.name: str = name
        self.mac_address: str = self.get_mac_address()
        self.mode = self.get_mode()

    def update(self) -> None:
        self.mac_address = self.get_mac_address()
        self.mode = self.get_mode()

    def get_mac_address(self) -> str:
        mac_address_file: str = f"/sys/class/net/{self.name}/address"
        if not os.path.exists(mac_address_file):
            raise FileNotFoundError("MAC address file not found.")
        with open(mac_address_file, "r") as file:
            mac_address: str = file.read().strip()
        return mac_address

    def get_mode(self) -> str:
        mode_file: str = f"/sys/class/net/{self.name}/type"
        if not os.path.exists(mode_file):
            raise FileNotFoundError("Mode file not found.")
        with open(mode_file, "r") as f:
            mode: str = f.read().strip()
        if mode == "1":
            return "managed"
        if mode == "803":
            return "monitor"

    def set_mode(self, mode: str, retries=3) -> bool:
        if mode not in ["managed", "monitor"]:
            return False
        if self.is_busy():
            self.reset()
            self.set_mode(mode, retries=retries-1)
        if mode == "monitor":
            self.down()
        cmd = f"sudo iwconfig {self.name} mode {mode}"
        result = subprocess.run(cmd.split(), capture_output=True)
        if result.returncode != 0:
            return False
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
            return False
        if not self.up():
            return False
        return True

    def is_busy(self) -> bool:
        cmd = f"ip link show {self.name}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if "state UP" in result.stdout and "state RUNNING" in result.stdout:
            return True
        else:
            return False

    def scan_access_points(self) -> List[str]:
        cmd = f"sudo iwlist {self.name} scan"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            return []
        output = result.stdout.strip().split('\n')
        access_points = []
        for i in range(len(output)):
            if "ESSID:" in output[i]:
                access_point = output[i].split(
                    "ESSID:")[1].strip().replace('"', '')
                access_points.append(access_point)
        return access_points

    def to_string(self) -> str:
        return f"Interface: {self.name}\nMAC Address: {self.mac_address}\nMode: {self.mode}"
