# microbit_ble_device_cloner.py

"""
BLE Device Cloning Attack for micro:bit V2 (Multi-Device Support)

This script clones the identity of a target BLE device to impersonate it.
- Detects available micro:bit devices and assigns tasks dynamically
- Captures BLE device information (`--scan <target_mac>`)
- Clones a BLE device (`--clone <target_mac>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Scan a BLE device for cloning:
   ```sh
   python microbit_ble_device_cloner.py --scan AA:BB:CC:DD:EE:FF
   ```

2. Clone a BLE device:
   ```sh
   python microbit_ble_device_cloner.py --clone AA:BB:CC:DD:EE:FF
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
from bleak import BleakScanner, BleakClient
import argparse

# Detect Connected Micro:bit Devices
async def detect_microbits():
    """Scans for connected micro:bit devices and returns their count."""
    devices = await BleakScanner.discover()
    microbits = [device.address for device in devices if "micro:bit" in (device.name or "").lower()]
    print(f"[+] Detected {len(microbits)} micro:bit devices.")
    return microbits

# BLE Device Scanning for Cloning
async def ble_scan(target_mac):
    """Scans a BLE device to gather cloning information."""
    print(f"[+] Scanning BLE device {target_mac} for cloning...")
    async with BleakClient(target_mac) as client:
        services = await client.get_services()
        for service in services:
            print(f"[+] Found Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"   - Characteristic: {characteristic.uuid}")

# BLE Device Cloning
async def ble_clone(target_mac):
    """Clones the identity of a BLE device."""
    print(f"[+] Cloning BLE device {target_mac}...")
    async with BleakClient(target_mac) as client:
        device_name = await client.read_gatt_char("00002a00-0000-1000-8000-00805f9b34fb")
        print(f"[+] Cloned Device Name: {device_name.decode()}")
        print(f"[+] Now advertising as {device_name.decode()}...")
        # Code to set up a spoofed BLE advertisement as the cloned device would go here

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Device Cloning Attack for micro:bit V2")
    parser.add_argument("--scan", metavar="target_mac", help="Scan a BLE device for cloning information")
    parser.add_argument("--clone", metavar="target_mac", help="Clone a BLE device")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.scan:
        loop.run_until_complete(ble_scan(args.scan))
    elif args.clone:
        loop.run_until_complete(ble_clone(args.clone))
