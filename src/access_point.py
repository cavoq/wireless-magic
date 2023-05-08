import subprocess
import time
from src.network_interface import NetworkInterface


class AccessPoint:

    def __init__(self, interface: NetworkInterface, ssid: str, password: str, channel: int = 6):
        self.interface = interface
        self.ssid = ssid
        self.password = password
        self.channel = channel

    def start(self) -> bool:
        if not self.interface.mode == "monitor":
            self.interface.set_mode("monitor")
        if not self._start_access_point():
            return False
        time.sleep(5)
        return True

    def stop(self) -> bool:
        cmd = ["sudo", "pkill", "hostapd"]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            return False

        if not self.interface.mode == "managed":
            self.interface.set_mode("managed")
        return True

    def _set_interface_mode(self, mode: str) -> bool:
        cmd = f"sudo iwconfig {self.interface} mode {mode}"
        result = subprocess.run(cmd.split(), capture_output=True)
        if result.returncode != 0:
            return False

        return True

    def _start_access_point(self) -> bool:
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

        config_file = f"/tmp/hostapd-{self.interface.name}.conf"
        with open(config_file, "w") as cfg_file:
            cfg_file.write(config)

        log_file = f"logs/{self.ssid}.log"
        cmd = ["sudo", "hostapd", config_file]

        with open(log_file, "w") as log:
            subprocess.Popen(cmd, stdout=log, stderr=log)

        return True
