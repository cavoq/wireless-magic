import os
from typing import List


def get_wifi_interfaces() -> List[str]:
    wifi_interfaces = []
    net_dir: str = "/sys/class/net"
    for interface in os.listdir(net_dir):
        if os.path.exists(os.path.join(net_dir, interface, "wireless")):
            wifi_interfaces.append(interface)
    return wifi_interfaces
