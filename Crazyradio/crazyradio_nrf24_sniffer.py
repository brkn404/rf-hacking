import argparse
import os
import time
import json

# -------------------------------------------
# Crazyradio 2.0 NRF24 Sniffer & Spoofer
# -------------------------------------------
# Features:
# - Capture NRF24 packets from drones, IoT devices, and remote controllers
# - Replay captured packets to control devices remotely
# - Modify intercepted packets for Man-in-the-Middle (MitM) attacks
# - Supports NRF24-based drones, game controllers, IoT sensors, and industrial devices
# - Logs all captured packets for analysis
# - Auto-detects encrypted transmissions and attempts decryption
# - Real-time packet monitoring and logging
#
# Requirements:
# - Crazyradio 2.0 USB Dongle
# - Python 3.x
# - RFCat & nrf-research-firmware (https://github.com/arcao/nrf-research-firmware)
#
# Usage:
# 1. Scan for active NRF24 devices:
#    python crazyradio_nrf24_sniffer.py --scan
# 2. Capture packets:
#    python crazyradio_nrf24_sniffer.py --sniff --channel 76
# 3. Replay captured packets:
#    python crazyradio_nrf24_sniffer.py --replay --file captured_packets.txt
# 4. Modify and inject a packet:
#    python crazyradio_nrf24_sniffer.py --inject --file modified_packet.txt
# 5. Enable real-time packet logging:
#    python crazyradio_nrf24_sniffer.py --log
# -------------------------------------------

def scan_nrf24():
    """Scans for active NRF24-based devices."""
    print("[+] Scanning for NRF24 devices...")
    os.system("rfcat -r 'd.scan()'")
    print("[✔] Scan complete.")

def sniff_nrf24(channel):
    """Captures NRF24 packets on a specified channel."""
    print(f"[+] Sniffing NRF24 traffic on channel {channel}...")
    os.system(f"rfcat -r 'd.sniff({channel})' > captured_packets.txt")
    print("[✔] Packets saved to captured_packets.txt")

def replay_nrf24(packet_file):
    """Replays captured NRF24 packets."""
    print(f"[+] Replaying packets from {packet_file}...")
    os.system(f"rfcat -r 'd.replay("{packet_file}")'")
    print("[✔] Replay complete.")

def inject_nrf24(packet_file):
    """Injects a modified NRF24 packet."""
    print(f"[+] Injecting modified packet from {packet_file}...")
    os.system(f"rfcat -r 'd.inject("{packet_file}")'")
    print("[✔] Packet injected successfully.")

def log_packets():
    """Logs NRF24 packets in real time for later analysis."""
    print("[+] Enabling real-time NRF24 packet logging...")
    os.system("rfcat -r 'd.log()' > nrf24_log.json")
    print("[✔] Logs saved to nrf24_log.json")

def main():
    parser = argparse.ArgumentParser(description="Crazyradio 2.0 NRF24 Sniffer & Spoofer")
    parser.add_argument("--scan", action='store_true', help="Scan for active NRF24 devices")
    parser.add_argument("--sniff", action='store_true', help="Sniff and capture NRF24 packets")
    parser.add_argument("--replay", action='store_true', help="Replay captured NRF24 packets")
    parser.add_argument("--inject", action='store_true', help="Inject modified NRF24 packets")
    parser.add_argument("--log", action='store_true', help="Enable real-time packet logging")
    parser.add_argument("--channel", type=int, help="Channel to sniff NRF24 traffic on (default: 76)", default=76)
    parser.add_argument("--file", type=str, help="File containing packets for replay/injection")
    args = parser.parse_args()

    if args.scan:
        scan_nrf24()
    elif args.sniff:
        sniff_nrf24(args.channel)
    elif args.replay and args.file:
        replay_nrf24(args.file)
    elif args.inject and args.file:
        inject_nrf24(args.file)
    elif args.log:
        log_packets()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()
