import multiprocessing
import time
from scapy.all import sniff
from scapy.layers.dot11 import Packet
from scapy.layers import dot11
from typing import Callable


class Sniffer:
    def __init__(self, iface_name: str, callback: Callable):
        self.iface_name = iface_name
        self.callback = callback
        self.sniffer_process = None

    def start(self):
        if self.sniffer_process is not None:
            return
        self.sniffer_process = multiprocessing.Process(
            target=self.sniff_packets)
        self.sniffer_process.start()

    def stop(self):
        if self.sniffer_process is not None:
            self.sniffer_process.terminate()
            self.sniffer_process.join()
            if self.sniffer_process.is_alive():
                raise Exception("Failed to stop sniffing process")
            self.sniffer_process = None

    def sniff_packets(self):
        sniff(iface=self.iface_name, prn=self.handle_packet)

    def handle_packet(self, packet: Packet):
        print(packet.summary())
        if packet.haslayer(dot11.Dot11Auth):
            self.callback(packet)

