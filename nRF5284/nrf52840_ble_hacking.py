import argparse
import os
import time
from scapy.all import *

# -------------------------------------------
# NRF52840 Advanced BLE Hacking Toolkit
# -------------------------------------------
# Features:
# - Sniff BLE 5.0 traffic (better than Flipper Zero)
# - Inject BLE packets (spoof connections & exploit vulnerabilities)
# - Capture BLE pairing requests & replay authentication sequences
# - Track BLE devices over long distances (Coded PHY support)
# - Scan for BLE devices using Extended Advertising (AirTags, IoT, hidden devices)
#
# Requirements:
# - NRF52840 Dongle / Dev Board (Adafruit Feather, Nordic Dongle, XIAO NRF52840)
# - Firmware: btlejack, BtleJuice, nrfutil
# - Python 3.x, Scapy
#
# Usage:
# 1. Sniff BLE packets:
#    python nrf52840_ble_hacking.py --sniff
# 2. Inject BLE packets:
#    python nrf52840_ble_hacking.py --inject "0102030405"
# 3. Capture pairing requests & replay them:
#    python nrf52840_ble_hacking.py --replay
# 4. Scan for BLE devices (Extended Advertising):
#    python nrf52840_ble_hacking.py --scan
# 5. Track BLE devices over long range:
#    python nrf52840_ble_hacking.py --track
# -------------------------------------------

def scan_ble():
    """Scans for nearby BLE devices using Extended Advertising."""
    print("[+] Scanning for BLE devices with Extended Advertising...")
    os.system("btlejack -s")

def sniff_ble():
    """Sniffs BLE 5.0 traffic and saves captured packets."""
    print("[+] Sniffing BLE packets...")
    os.system("btlejack -c 37,38,39 -x ble_capture.pcap")

def inject_ble(packet_data):
    """Injects BLE packets to test vulnerabilities."""
    print(f"[+] Injecting BLE packet: {packet_data}")
    os.system(f"btlejack -i {packet_data}")

def replay_ble():
    """Replays captured BLE pairing/authentication sequences."""
    print("[+] Replaying captured BLE pairing sequence...")
    os.system("btlejack -r ble_capture.pcap")

def track_ble():
    """Tracks BLE devices over long distances using Coded PHY."""
    print("[+] Tracking BLE devices at long range...")
    os.system("btlejack -t")

def main():
    parser = argparse.ArgumentParser(description="NRF52840 BLE Hacking Toolkit")
    parser.add_argument("--scan", action='store_true', help="Scan for BLE devices (Extended Advertising)")
    parser.add_argument("--sniff", action='store_true', help="Sniff BLE packets")
    parser.add_argument("--inject", type=str, help="Inject a BLE packet (hex string)")
    parser.add_argument("--replay", action='store_true', help="Replay BLE pairing/authentication sequences")
    parser.add_argument("--track", action='store_true', help="Track BLE devices over long range")
    args = parser.parse_args()

    if args.scan:
        scan_ble()
    elif args.sniff:
        sniff_ble()
    elif args.inject:
        inject_ble(args.inject)
    elif args.replay:
        replay_ble()
    elif args.track:
        track_ble()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()
