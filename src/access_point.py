import subprocess
import threading
import time
from scapy.all import sniff, sendp
from scapy.layers import dot11
from scapy.layers.dot11 import Packet
from src.sniffer import Sniffer
from src.network_interface import NetworkInterface


class AccessPoint:

    def __init__(self, interface: NetworkInterface, ssid: str, password: str, channel: int = 6):
        self.interface = interface
        self.ssid = ssid
        self.password = password
        self.channel = channel
        self.sniffer = Sniffer(self.interface.name, handle_packet)

    def to_string(self) -> str:
        return f"SSID: {self.ssid}\nPassword: {self.password}\nChannel: {self.channel}"

    def start(self) -> bool:
        if not self.interface.get_mode() == "monitor":
            self.interface.set_mode("monitor")
        if not self.start_access_point():
            raise Exception("Failed to start access point")
        return True

    def stop(self) -> bool:
        cmd = ["sudo", "pkill", "hostapd"]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            raise Exception("Failed to stop access point")
        if not self.interface.get_mode() == "managed":
            self.interface.set_mode("managed")
        return True

    def start_access_point(self) -> bool:
        with open("resources/hostapd-template.conf", "r") as f:
            config_template = f.read()

        config = config_template.replace(
            "place_interface_here", self.interface.name
        ).replace(
            "place_ssid_here", self.ssid
        ).replace(
            "place_channel_here", str(self.channel)
        ).replace(
            "place_password_here", self.password
        )

        config_file = f"hostapd-configs/hostapd-{self.interface.name}.conf"
        with open(config_file, "w") as cfg_file:
            cfg_file.write(config)

        log_file = f"logs/{self.ssid}.log"
        cmd = ["sudo", "hostapd", config_file]

        with open(log_file, "w") as log:
            subprocess.Popen(cmd, stdout=log, stderr=log)

        time.sleep(1)  # Wait for hostapd to start
        return True


def handle_packet(pkt: Packet) -> None:
    print(pkt.summary())
