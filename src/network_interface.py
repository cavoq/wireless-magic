import os
import subprocess
from typing import List


class NetworkInterface:
    def __init__(self, interface: str):
        self.interface: str = interface
        self.mac_address: str = self.get_mac_address()
        self.mode = self.get_mode()

    def update(self) -> None:
        self.mac_address = self.get_mac_address()
        self.mode = self.get_mode()
    
    def get_mac_address(self) -> str:
        mac_address_file: str = f"/sys/class/net/{self.interface}/address"
        with open(mac_address_file, "r") as f:
            mac_address: str = f.read().strip()
        return mac_address

    def get_mode(self) -> str:
        mode_file: str = f"/sys/class/net/{self.interface}/type"
        with open(mode_file, "r") as f:
            mode: str = f.read().strip()
        if mode == "1":
            return "Managed"
        if mode == "803":
            return "Monitor"

    def set_mode(self, mode: str) -> bool:
        if mode != ("managed" or "monitor"):
            return False
        cmd = f"sudo iwconfig {self.interface} mode {mode}"
        result = subprocess.run(cmd.split(), capture_output=True)
        if result.returncode != 0:
            return False
        return True
            
    def to_string(self) -> str:
        return f"Interface: {self.interface}\nMAC Address: {self.mac_address}\nMode: {self.mode}"


def get_wifi_interfaces() -> List[NetworkInterface]:
    wifi_interfaces = []
    net_dir: str = "/sys/class/net"
    for interface in os.listdir(net_dir):
        if os.path.exists(os.path.join(net_dir, interface, "wireless")):
            wifi_interfaces.append(NetworkInterface(interface))
    return wifi_interfaces
