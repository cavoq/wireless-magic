import os
import subprocess
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
        with open(mac_address_file, "r") as f:
            mac_address: str = f.read().strip()
        return mac_address

    def get_mode(self) -> str:
        mode_file: str = f"/sys/class/net/{self.name}/type"
        with open(mode_file, "r") as f:
            mode: str = f.read().strip()
        if mode == "1":
            return "managed"
        if mode == "803":
            return "monitor"

    def set_mode(self, mode: str) -> bool:
        if mode != ("managed" or "monitor"):
            return False
        cmd = f"sudo iwconfig {self.interface} mode {mode}"
        result = subprocess.run(cmd.split(), capture_output=True)
        if result.returncode != 0:
            return False
        return True

    def scan_access_points(self) -> List[str]:
        cmd = f"sudo iwlist {self.name} scan"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            return []
        output = result.stdout.strip().split('\n')
        access_points = []
        for i in range(len(output)):
            if "ESSID:" in output[i]:
                access_point = output[i].split("ESSID:")[1].strip().replace('"', '')
                access_points.append(access_point)
        return access_points
    
    def to_string(self) -> str:
        return f"Interface: {self.name}\nMAC Address: {self.mac_address}\nMode: {self.mode}"
