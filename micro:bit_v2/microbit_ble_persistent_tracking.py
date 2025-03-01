# microbit_ble_persistent_tracking.py

"""
Persistent BLE Tracking & Surveillance for micro:bit V2 (Multi-Device Support)

This script continuously monitors and tracks BLE devices in a target area.
- Detects available micro:bit devices and distributes tasks dynamically
- Persistent BLE scanning (`--scan`)
- Logs BLE device movement (`--track <mac> --log <file>`)
- Identifies hidden BLE devices (`--find-hidden`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Continuously scan for BLE devices:
   ```sh
   python microbit_ble_persistent_tracking.py --scan
   ```

2. Track a specific BLE device over time:
   ```sh
   python microbit_ble_persistent_tracking.py --track AA:BB:CC:DD:EE:FF --log movement_log.json
   ```

3. Identify hidden BLE devices:
   ```sh
   python microbit_ble_persistent_tracking.py --find-hidden
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
from bleak import BleakScanner
import argparse
import json

# Detect Connected Micro:bit Devices
async def detect_microbits():
    """Scans for connected micro:bit devices and returns their count."""
    devices = await BleakScanner.discover()
    microbits = [device.address for device in devices if "micro:bit" in (device.name or "").lower()]
    print(f"[+] Detected {len(microbits)} micro:bit devices.")
    return microbits

# Continuous BLE Scan
async def ble_scan():
    """Continuously scans for BLE devices and logs their presence."""
    print("[+] Starting persistent BLE scanning...")
    while True:
        devices = await BleakScanner.discover()
        for device in devices:
            print(f"[+] Found {device.address} - {device.name} - RSSI: {device.rssi}")
        await asyncio.sleep(5)

# Track BLE Device Movement
async def ble_track(target_mac, log_file):
    """Tracks a BLE device's movement based on RSSI changes."""
    print(f"[+] Tracking BLE device {target_mac}...")
    movement_log = []
    while True:
        devices = await BleakScanner.discover()
        for device in devices:
            if device.address == target_mac:
                print(f"[+] Tracking {device.address}: RSSI {device.rssi}")
                movement_log.append({"address": target_mac, "rssi": device.rssi})
                if log_file:
                    with open(log_file, "w") as f:
                        json.dump(movement_log, f)
                        print(f"[+] Movement log updated: {log_file}")
        await asyncio.sleep(5)

# Identify Hidden BLE Devices
async def find_hidden_ble():
    """Scans for BLE devices using weak advertisements or hidden signals."""
    print("[+] Scanning for hidden BLE devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        if not device.name:
            print(f"[+] Hidden BLE device detected: {device.address} - RSSI: {device.rssi}")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Persistent BLE Tracking & Surveillance for micro:bit V2")
    parser.add_argument("--scan", help="Continuously scan for BLE devices", action="store_true")
    parser.add_argument("--track", help="Track a specific BLE device's movement", metavar="target_mac")
    parser.add_argument("--log", help="Log tracked BLE device movements", metavar="log_file")
    parser.add_argument("--find-hidden", help="Identify hidden BLE devices", action="store_true")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.scan:
        loop.run_until_complete(ble_scan())
    elif args.track:
        loop.run_until_complete(ble_track(args.track, args.log))
    elif args.find_hidden:
        loop.run_until_complete(find_hidden_ble())
