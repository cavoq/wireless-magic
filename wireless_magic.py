import cmd
import re
from typing import Dict, List
import colorama
from src.network_interface import *
from src.access_point import *
from src.config import Config
from src.log import logger

CONFIG_FILE = "config.json"

colorama.init()


class WirelessMagicCmd(cmd.Cmd):
    intro = f"""{colorama.Fore.GREEN}
          _          _                                            _      
         (_)        | |                                          (_)     
__      ___ _ __ ___| | ___  ___ ___        _ __ ___   __ _  __ _ _  ___ 
\ \ /\ / / | '__/ _ \ |/ _ \/ __/ __|______| '_ ` _ \ / _` |/ _` | |/ __|
 \ V  V /| | | |  __/ |  __/\__ \__ \______| | | | | | (_| | (_| | | (__ 
  \_/\_/ |_|_|  \___|_|\___||___/___/      |_| |_| |_|\__,_|\__, |_|\___|
                                                             __/ |       
                                                            |___/        
                                                            
[+] Welcome to wireless-magic, a tool to simplify wireless network operations.
[cls] Clear the screen.
[q] Quit the program.
[i] Get list of available network interfaces.
[is <interface_name>] Set capture interface.
[ap] Get list of available access points.
{colorama.Style.RESET_ALL}"""
    prompt = f"{colorama.Fore.BLUE}> {colorama.Style.RESET_ALL}"

    def do_cls(self, arg=None):
        print(self.intro)

    def do_q(self, arg=None):
        print(f"{colorama.Fore.RED}Quitting...{colorama.Style.RESET_ALL}")
        logger.info("Stopping wireless-magic...")
        return True

    def do_i(self, arg=None):
        for interface in wireless_magic.get_wifi_interfaces():
            print(f"{colorama.Fore.GREEN}{interface.to_string()}", end="\n\n")

    def do_is(self, arg=None):
        if wireless_magic.capture_interface is not None and arg in [None, ""]:
            print(
                f"{colorama.Fore.RED}Selected interface is {wireless_magic.capture_interface.name}.{colorama.Style.RESET_ALL}")
            return
        if arg not in [interface.name for interface in wireless_magic.wifi_interfaces]:
            print(
                f"{colorama.Fore.RED}Please specify a valid interface.{colorama.Style.RESET_ALL}")
            return
        wireless_magic.set_capture_interface(arg)
        print(f"{colorama.Fore.GREEN}Interface set to {arg}.{colorama.Style.RESET_ALL}")

    def do_ap(self, arg=None):
        if wireless_magic.capture_interface is None:
            print(
                f"{colorama.Fore.RED}Please select an interface first.{colorama.Style.RESET_ALL}")
            return
        wireless_magic.scan_access_points()
        for access_point in wireless_magic.access_points.values():
            print(f"{colorama.Fore.GREEN}{access_point.to_string()}", end="\n\n")


class WirelessMagic:

    def __init__(self):
        self.wifi_interfaces: List[NetworkInterface] = self.get_wifi_interfaces(
        )
        self.access_points: Dict[str, AccessPoint] = {}
        self.capture_interface: NetworkInterface = None

    def get_wifi_interfaces(self) -> List[NetworkInterface]:
        logger.info("Getting wifi interfaces...")
        wifi_interfaces = []
        net_dir: str = "/sys/class/net"
        for interface in os.listdir(net_dir):
            if os.path.exists(os.path.join(net_dir, interface, "wireless")):
                wifi_interfaces.append(NetworkInterface(interface))
        logger.info(f"Found {len(wifi_interfaces)} wifi interfaces.")
        return wifi_interfaces

    def set_capture_interface(self, interface_name: str) -> bool:
        logger.info(f"Setting capture interface to {interface_name}...")
        for interface in self.wifi_interfaces:
            if interface.name == interface_name:
                self.capture_interface = interface
                logger.info(f"Capture interface set to {interface_name}.")
                return True
        logger.warning(f"Interface {interface_name} not found.")
        return False

    def scan_access_points(self) -> None:
        logger.info(
            f"Scanning for access points on {self.capture_interface.name}...")
        cmd = f"sudo iwlist {self.capture_interface.name} scan"
        output = subprocess.check_output(cmd.split()).decode("utf-8")

        essids = re.findall(r"ESSID:\"(.*)\"", output)
        channels = re.findall(r"Channel:(\d+)", output)
        mac_addresses = re.findall(r"Address: ([0-9A-F:]+)", output)

        for essid, channel, mac_address in zip(essids, channels, mac_addresses):
            access_point = AccessPoint(
                self.capture_interface, essid, "pass", mac_address, channel)
            self.access_points[essid] = access_point
        logger.info(f"Found {len(self.access_points)} access points.")


if __name__ == '__main__':
    Config().from_json(CONFIG_FILE)
    wireless_magic: WirelessMagic = WirelessMagic()
    WirelessMagicCmd().cmdloop()
