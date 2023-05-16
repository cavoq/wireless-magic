import threading
from scapy.all import sniff
from scapy.layers.dot11 import Packet
from scapy.layers import dot11
from typing import Callable


class Sniffer:
    def __init__(self, iface_name: str, callback: Callable):
        self.iface_name = iface_name
        self.callback = callback
        self.sniffer_thread = None

    def start(self):
        if self.sniffer_thread is not None:
            return
        self.sniffer_thread = threading.Thread(
            target=self.sniff_packets, daemon=True)
        self.sniffer_thread.start()

    def stop(self):
        if self.sniffer_thread is not None:
            self.sniffer_thread.join()
            self.sniffer_thread = None

    def sniff_packets(self):
        sniff(iface=self.iface_name, prn=self.handle_packet)

    def handle_packet(self, packet: Packet):
        print(packet.summary())
        if packet.haslayer(dot11.Dot11Auth):
            self.callback(packet)
