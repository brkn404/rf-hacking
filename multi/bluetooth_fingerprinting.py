import argparse
import subprocess
import logging
from collections import defaultdict

# -------------------------------------------
# Bluetooth Device Fingerprinting Tool
# -------------------------------------------
# Features:
# - Discover Bluetooth devices and extract metadata.
# - Analyze MAC addresses, RSSI patterns, and service UUIDs.
# - Identify specific device models and detect spoofed devices.
# - Log all actions and results.
#
# Requirements:
# - nRF52840 Dongle or Ubertooth One
# - Python 3.x
# - nRF Util (nrfutil) or Ubertooth tools
#
# Usage:
# 1. Discover and fingerprint all devices:
#    python bluetooth_fingerprinting.py --discover --interface nrf52840
# 2. Fingerprint a specific device:
#    python bluetooth_fingerprinting.py --fingerprint XX:XX:XX:XX:XX:XX --interface nrf52840
# -------------------------------------------

# Global variables
logging.basicConfig(filename="bluetooth_fingerprinting.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_event(message):
    """Log an event to the log file."""
    logging.info(message)
    print(message)

def discover_devices(interface):
    """
    Discover Bluetooth devices and extract metadata.
    :param interface: Interface to use (nrf52840 or ubertooth).
    """
    log_event("[+] Discovering Bluetooth devices...")
    devices = defaultdict(dict)
    try:
        if interface == "nrf52840":
            command = "nrfutil scanner --discover"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        elif interface == "ubertooth":
            command = "ubertooth-scan"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        else:
            log_event("[!] Invalid interface specified. Use 'nrf52840' or 'ubertooth'.")
            return

        # Parse output and extract device metadata
        for line in result.stdout.splitlines():
            if "MAC:" in line:
                mac = line.split("MAC:")[1].strip()
                devices[mac]["mac"] = mac
            elif "RSSI:" in line:
                rssi = line.split("RSSI:")[1].strip()
                devices[mac]["rssi"] = rssi
            elif "UUID:" in line:
                uuid = line.split("UUID:")[1].strip()
                devices[mac]["uuid"] = uuid

        log_event(f"[✔] Discovered {len(devices)} devices.")
        for mac, metadata in devices.items():
            log_event(f"[*] Device: {mac}, RSSI: {metadata.get('rssi', 'N/A')}, UUID: {metadata.get('uuid', 'N/A')}")
    except subprocess.CalledProcessError as e:
        log_event(f"[!] Error during device discovery: {e}")

def fingerprint_device(mac_address, interface):
    """
    Fingerprint a specific Bluetooth device.
    :param mac_address: MAC address of the target device.
    :param interface: Interface to use (nrf52840 or ubertooth).
    """
    log_event(f"[+] Fingerprinting device {mac_address}...")
    try:
        if interface == "nrf52840":
            command = f"nrfutil scanner --filter {mac_address} --fingerprint"
        elif interface == "ubertooth":
            command = f"ubertooth-scan --filter {mac_address}"
        else:
            log_event("[!] Invalid interface specified. Use 'nrf52840' or 'ubertooth'.")
            return

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        log_event(f"[✔] Fingerprinting results for {mac_address}:")
        log_event(result.stdout)
    except subprocess.CalledProcessError as e:
        log_event(f"[!] Error during fingerprinting: {e}")

def main():
    parser = argparse.ArgumentParser(description="Bluetooth Device Fingerprinting Tool")
    parser.add_argument("--discover", action="store_true", help="Discover Bluetooth devices")
    parser.add_argument("--fingerprint", type=str, help="Fingerprint a specific device by MAC address")
    parser.add_argument("--interface", type=str, required=True, help="Interface to use (nrf52840 or ubertooth)")
    args = parser.parse_args()

    if args.discover:
        discover_devices(args.interface)
    elif args.fingerprint:
        fingerprint_device(args.fingerprint, args.interface)
    else:
        log_event("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()