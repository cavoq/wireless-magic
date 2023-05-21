import cmd
import re
from typing import Dict, List
import colorama
from src.network_interface import *
from src.access_point import *
from src.config import Config

CONFIG_FILE = "config.json"

colorama.init()


class TwinerCmd(cmd.Cmd):
    intro = f"""{colorama.Fore.GREEN}
__________       _____________     __________________
\__   __/|\     /|\__   __/( (    /|(  ____ \(  ____ )
   ) (   | )   ( |   ) (   |  \  ( || (    \/| (    )|
   | |   | | _ | |   | |   |   \ | || (__    | (____)|
   | |   | |( )| |   | |   | (\ \) ||  __)   |     __)
   | |   | || || |   | |   | | \   || (      | (\ (   
   | |   | () () |___) (___| )  \  || (____/\| ) \ \__
   )_(   (_______)\_______/|/    )_)(_______/|/   \__/
   
   
[+] Welcome to Twiner, a rogue access points attack bot.
[clear] Clear the screen.
[quit] Quit the program.
[ifaces] Get list of available network interfaces.
[iface <interface>] Set the network interface to use.
[run] Run the bot.
{colorama.Style.RESET_ALL}"""
    prompt = f"{colorama.Fore.BLUE}> {colorama.Style.RESET_ALL}"

    def do_clear(self, arg=None):
        print(self.intro)

    def do_quit(self, arg=None):
        print(f"{colorama.Fore.RED}Quitting...{colorama.Style.RESET_ALL}")
        return True

    def do_ifaces(self, arg=None):
        for interface in twiner_bot.wifi_interfaces:
            print(f"{colorama.Fore.GREEN}{interface.to_string()}", end="\n\n")

    def do_iface(self, arg=None):
        if twiner_bot.capture_interface is not None and arg in [None, ""]:
            print(
                f"{colorama.Fore.RED}Selected interface is {twiner_bot.capture_interface.name}.{colorama.Style.RESET_ALL}")
            return
        if arg not in [interface.name for interface in twiner_bot.wifi_interfaces]:
            print(
                f"{colorama.Fore.RED}Please specify a valid interface.{colorama.Style.RESET_ALL}")
            return
        twiner_bot.set_capture_interface(arg)
        print(f"{colorama.Fore.GREEN}Interface set to {arg}.{colorama.Style.RESET_ALL}")

    def do_run(self, arg=None):
        twiner_bot.scan_access_points()
        twiner_bot.run()


class TwinerBot:

    def __init__(self):
        self.wifi_interfaces: List[NetworkInterface] = self.get_wifi_interfaces(
        )
        self.access_points: Dict[str, AccessPoint] = {}
        self.capture_interface: NetworkInterface = None

    def run(self):
        self.access_points["TestAP"] = AccessPoint(
            self.capture_interface, "TestAP", "testpassword", 6)
        self.access_points.get("TestAP").start()
        self.access_points.get("TestAP").start_sniffing()

    def get_wifi_interfaces(self) -> List[NetworkInterface]:
        wifi_interfaces = []
        net_dir: str = "/sys/class/net"
        for interface in os.listdir(net_dir):
            if os.path.exists(os.path.join(net_dir, interface, "wireless")):
                wifi_interfaces.append(NetworkInterface(interface))
        return wifi_interfaces

    def set_capture_interface(self, interface_name: str) -> bool:
        for interface in self.wifi_interfaces:
            if interface.name == interface_name:
                self.capture_interface = interface
                return True
        return False

    def scan_access_points(self) -> None:
        cmd = f"sudo iwlist {self.capture_interface.name} scan"
        output = subprocess.check_output(cmd.split()).decode("utf-8")

        essids = re.findall(r"ESSID:\"(.*)\"", output)
        channels = re.findall(r"Channel:(\d+)", output)

        for essid, channel in zip(essids, channels):
            access_point = AccessPoint(
                self.capture_interface, essid, "pass", channel)
            self.access_points[essid] = access_point


if __name__ == '__main__':
    Config().from_json(CONFIG_FILE)
    twiner_bot: TwinerBot = TwinerBot()
    TwinerCmd().cmdloop()
