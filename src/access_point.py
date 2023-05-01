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
            return False
        if not self._start_access_point():
            return False

        time.sleep(5)

        if not self._set_interface_mode("managed"):
            return False

        return True

    def stop(self) -> bool:
        cmd = ["sudo", "pkill", "hostapd"]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            return False

        return True

    def _set_interface_mode(self, mode: str) -> bool:
        cmd = f"sudo iwconfig {self.interface} mode {mode}"
        result = subprocess.run(cmd.split(), capture_output=True)
        if result.returncode != 0:
            return False

        return True

    def _start_access_point(self) -> bool:
        config = f"""
        interface={self.interface.name}
        driver=nl80211
        ssid={self.ssid}
        hw_mode=g
        channel={self.channel}
        macaddr_acl=0
        auth_algs=1
        ignore_broadcast_ssid=0
        wpa=2
        wpa_passphrase={self.password}
        wpa_key_mgmt=WPA-PSK
        wpa_pairwise=TKIP
        rsn_pairwise=CCMP
        """
        config_file = f"/tmp/hostapd-{self.interface.name}.conf"
        with open(config_file, "w") as f:
            f.write(config)

        cmd = ["sudo", "hostapd", config_file]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            return False

        return True
